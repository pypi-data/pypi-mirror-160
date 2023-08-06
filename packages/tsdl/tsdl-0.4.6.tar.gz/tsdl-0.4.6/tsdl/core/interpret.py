from importlib import import_module

from tsdl.common import util
from tsdl.core.context import Context
from tsdl.logger.log import logger


def handle(context: Context):
    try:
        model = import_module(context.script)
        sorted_steps_no, steps = extract_steps_from_model(dir(model))
        sorted_steps_no = sorted(sorted_steps_no)

        index = 0

        while index < len(sorted_steps_no):
            step_no = sorted_steps_no[index]

            if meet_loops(context, int(step_no)):
                index = loop_steps(context, model, steps, index)
                context.runtime.reset_loop()
            else:
                exec_step(context, model, steps.get(str(step_no)))

            index += 1
    finally:
        context.cache.clear()


def extract_steps_from_model(steps: list):
    n_s = []
    m_d = {}
    for s in steps:
        if s.upper().find('STEP_') >= 0:
            n = util.extract_digit(s)
            n_s.append(int(n))
            m_d[n] = s

    sorted_n_s = sorted(n_s)

    return sorted_n_s, m_d


def meet_loops(context: Context, step_no):
    try:
        lp = context.loops[0]

        if lp.count > 0:
            context.runtime.loop_times = lp.count

        if context.runtime.loop_times <= 0:
            return False
        if lp.range.start <= 0:
            return False
        if lp.range.end <= 0:
            return False
        if lp.range.start > lp.range.end:
            return False

        context.runtime.loop_range_start = lp.range.start
        context.runtime.loop_range_end = lp.range.end

        if lp.range.start <= step_no <= lp.range.end:
            return True
    except IndexError as e:
        logger.error(str(e))
        return False
    except Exception as ee:
        logger.error(str(ee))
        return False

    return False


def loop_steps(context: Context, model, steps: dict, index: int):
    blank = 0
    context.loops.pop(0)
    logger.info('~ &LOOPS START -step_range {}-{} -count {}'.format(context.runtime.loop_range_start,
                                                                    context.runtime.loop_range_end,
                                                                    context.runtime.loop_times))
    for i in range(context.runtime.loop_times):
        logger.info('~ &&LOOP start to run no.{}, total.{} '.format(i + 1, context.runtime.loop_times))
        blank = 0
        for j in range(context.runtime.loop_range_start, context.runtime.loop_range_end + 1):
            step = steps.get(str(j))
            if step is not None:
                exec_step(context, model, step)
            else:
                blank += 1
        context.runtime.loop_index = i + 1
    logger.info('~ &LOOPS END.')

    return index + (context.runtime.loop_range_end - context.runtime.loop_range_start) - blank


def exec_step(context: Context, model, step: str):
    try:
        logger.info('~ #{}# start to run'.format(step.upper()))
        context.runtime.step = step

        result = getattr(model, '{}'.format(step))(context)
        if result is not None:
            context.runtime.last_result = result
    except AssertionError as ae:
        raise ae
    except Exception as e:
        logger.error(str(e))

