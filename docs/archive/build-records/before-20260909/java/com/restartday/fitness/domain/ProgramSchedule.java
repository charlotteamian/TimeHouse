package com.restartday.fitness.domain;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * 把 8 周周期计划展开成绑日期的训练日历。
 *
 * <p>以前只有 {@code "周:日"} 这种没有日期的键，漏练自动顺延——8 周计划会无声地拉长，
 * 而周期化的强度曲线是按周设计的，顺延等于把曲线拉平。
 *
 * <p>这里的策略是**保持周结构**：漏了就是漏了，标记 MISSED，本周剩余照常；
 * 一周过完如果完成率低于 {@link #REPEAT_WEEK_THRESHOLD}，提示把这一周重做一次
 * （由用户确认，不静默改日历）。
 */
public final class ProgramSchedule {

    /** 一周完成率低于这个比例就建议重做该周，而不是顺延。 */
    public static final double REPEAT_WEEK_THRESHOLD = 0.6;

    /** 连续两周低于这个比例就该下调每周天数、重新生成计划。 */
    public static final double REPLAN_THRESHOLD = 0.5;

    private final List<ScheduledSession> sessions;

    public ProgramSchedule(List<ScheduledSession> sessions) {
        List<ScheduledSession> copy = new ArrayList<ScheduledSession>(sessions);
        Collections.sort(copy, new Comparator<ScheduledSession>() {
            @Override
            public int compare(ScheduledSession left, ScheduledSession right) {
                int byDate = Long.compare(left.epochDay(), right.epochDay());
                return byDate != 0 ? byDate : Integer.compare(left.dayIndex(), right.dayIndex());
            }
        });
        this.sessions = Collections.unmodifiableList(copy);
    }

    public List<ScheduledSession> sessions() {
        return sessions;
    }

    public boolean isEmpty() {
        return sessions.isEmpty();
    }

    /** 每周训练天数对应的默认星期（ISO：1=周一 … 7=周日），尽量隔天练。 */
    public static List<Integer> defaultWeekdays(int daysPerWeek) {
        switch (Math.max(2, Math.min(5, daysPerWeek))) {
            case 2:
                return Arrays.asList(2, 5);
            case 3:
                return Arrays.asList(1, 3, 5);
            case 4:
                return Arrays.asList(1, 2, 4, 5);
            default:
                return Arrays.asList(1, 2, 3, 5, 6);
        }
    }

    /** 编排一天动作的回调，让调用方决定用本地槽位编排还是 AI 参与。 */
    public interface DayComposer {
        /**
         * @param recentIds 之前几天已经排过的动作 id，按时间倒序（下标 0 = 最近），用于跨天去重
         * @return 该日的动作 id 与对应槽位；返回 null 表示排不出来
         */
        ProgramComposer.ComposedDay compose(int week, int dayIndex, ProgramFocus focus,
                ProgramPhase phase, List<String> recentIds);
    }

    /**
     * 展开整个计划：从 {@code startEpochDay} 当周开始，按 weekdays 落到具体日期，
     * 逐日调用 composer 预生成动作（这样日历上才有内容可看，也才能保证跨天不重复）。
     */
    public static ProgramSchedule build(TrainingProgram program, long startEpochDay,
            List<Integer> weekdays, DayComposer composer) {
        List<Integer> days = weekdays == null || weekdays.isEmpty()
                ? defaultWeekdays(program.daysPerWeek())
                : new ArrayList<Integer>(weekdays);
        // 选的天数不够就用默认排布补齐，否则两次训练会撞到同一天。
        for (Integer weekday : defaultWeekdays(program.daysPerWeek())) {
            if (days.size() >= program.daysPerWeek()) {
                break;
            }
            if (!days.contains(weekday)) {
                days.add(weekday);
            }
        }
        Collections.sort(days);
        long weekAnchor = startOfWeek(startEpochDay);
        List<ScheduledSession> result = new ArrayList<ScheduledSession>();
        List<String> recentIds = new ArrayList<String>();

        for (int week = 1; week <= program.totalWeeks(); week++) {
            ProgramPhase phase = program.phaseForWeek(week);
            for (int dayIndex = 0; dayIndex < program.daysPerWeek(); dayIndex++) {
                int weekday = days.get(Math.min(dayIndex, days.size() - 1));
                long date = weekAnchor + (week - 1) * 7L + (weekday - 1);
                if (date < startEpochDay) {
                    // 生成当天之前的格子直接顺到下一周，避免开局就是一堆已漏练。
                    date += 7L;
                }
                ProgramFocus focus = program.focusForDay(dayIndex);
                ProgramComposer.ComposedDay day = composer.compose(week, dayIndex, focus, phase, recentIds);
                List<String> ids = day == null
                        ? new ArrayList<String>() : new ArrayList<String>(day.exerciseIds());
                List<String> slots = day == null
                        ? new ArrayList<String>() : new ArrayList<String>(day.slotKeys());
                result.add(new ScheduledSession(week, dayIndex, date, focus, ids, slots,
                        ScheduledSession.Status.PLANNED, false));
                for (int i = ids.size() - 1; i >= 0; i--) {
                    recentIds.remove(ids.get(i));
                    recentIds.add(0, ids.get(i));
                }
            }
        }
        return new ProgramSchedule(result);
    }

    /** 日期已过但仍是 PLANNED 的标记为 MISSED。不顺延。 */
    public ProgramSchedule markMissedBefore(long todayEpochDay) {
        List<ScheduledSession> updated = new ArrayList<ScheduledSession>(sessions.size());
        for (ScheduledSession session : sessions) {
            if (session.epochDay() < todayEpochDay
                    && session.status() == ScheduledSession.Status.PLANNED) {
                updated.add(session.withStatus(ScheduledSession.Status.MISSED));
            } else {
                updated.add(session);
            }
        }
        return new ProgramSchedule(updated);
    }

    /** 今天该练的那次；今天没有安排就返回最近的一次未完成安排。 */
    public ScheduledSession todayOrNext(long todayEpochDay) {
        for (ScheduledSession session : sessions) {
            if (session.epochDay() == todayEpochDay
                    && session.status() == ScheduledSession.Status.PLANNED) {
                return session;
            }
        }
        for (ScheduledSession session : sessions) {
            if (session.epochDay() > todayEpochDay
                    && session.status() == ScheduledSession.Status.PLANNED) {
                return session;
            }
        }
        return null;
    }

    public ScheduledSession byKey(String key) {
        for (ScheduledSession session : sessions) {
            if (session.key().equals(key)) {
                return session;
            }
        }
        return null;
    }

    public List<ScheduledSession> onDate(long epochDay) {
        List<ScheduledSession> result = new ArrayList<ScheduledSession>();
        for (ScheduledSession session : sessions) {
            if (session.epochDay() == epochDay) {
                result.add(session);
            }
        }
        return result;
    }

    public ProgramSchedule withSession(ScheduledSession updated) {
        List<ScheduledSession> result = new ArrayList<ScheduledSession>(sessions.size());
        for (ScheduledSession session : sessions) {
            result.add(session.key().equals(updated.key()) ? updated : session);
        }
        return new ProgramSchedule(result);
    }

    public int doneCount() {
        int count = 0;
        for (ScheduledSession session : sessions) {
            if (session.status() == ScheduledSession.Status.DONE) {
                count++;
            }
        }
        return count;
    }

    public int totalCount() {
        return sessions.size();
    }

    /** 某一周的完成率（DONE / 该周总数）；跳过算没完成。 */
    public double weekCompletion(int week, boolean repeatWeek) {
        int total = 0;
        int done = 0;
        for (ScheduledSession session : sessions) {
            if (session.week() == week && session.isRepeatWeek() == repeatWeek) {
                total++;
                if (session.status() == ScheduledSession.Status.DONE) {
                    done++;
                }
            }
        }
        return total == 0 ? 1.0 : done / (double) total;
    }

    /**
     * 已经完全过去、完成率不足、且还没重做过的周。返回最早的一个，没有则返回 0。
     * 调用方应该拿它去问用户要不要重做，而不是静默改日历。
     */
    public int weekNeedingRepeat(long todayEpochDay) {
        for (int week = 1; week <= 52; week++) {
            long lastDay = -1;
            boolean exists = false;
            boolean alreadyRepeated = false;
            for (ScheduledSession session : sessions) {
                if (session.week() != week) {
                    continue;
                }
                if (session.isRepeatWeek()) {
                    alreadyRepeated = true;
                    continue;
                }
                exists = true;
                lastDay = Math.max(lastDay, session.epochDay());
            }
            if (!exists) {
                if (week > 1) {
                    break;
                }
                continue;
            }
            if (alreadyRepeated || lastDay >= todayEpochDay) {
                continue;
            }
            if (weekCompletion(week, false) < REPEAT_WEEK_THRESHOLD) {
                return week;
            }
        }
        return 0;
    }

    /**
     * 把某一周原样重做一次：复制该周的安排插到它后面，之后的所有安排整体后移 7 天。
     * 强度曲线按周设计，所以是"重复一周"而不是"把漏掉的那次挪到后面"。
     */
    public ProgramSchedule repeatWeek(int week) {
        long lastDay = -1;
        for (ScheduledSession session : sessions) {
            if (session.week() == week && !session.isRepeatWeek()) {
                lastDay = Math.max(lastDay, session.epochDay());
            }
        }
        if (lastDay < 0) {
            return this;
        }
        List<ScheduledSession> result = new ArrayList<ScheduledSession>();
        for (ScheduledSession session : sessions) {
            if (session.epochDay() > lastDay) {
                result.add(session.withDate(session.epochDay() + 7L));
            } else {
                result.add(session);
            }
            if (session.week() == week && !session.isRepeatWeek()) {
                result.add(new ScheduledSession(week, session.dayIndex(), session.epochDay() + 7L,
                        session.focus(), session.exerciseIds(), session.slotKeys(),
                        ScheduledSession.Status.PLANNED, true));
            }
        }
        return new ProgramSchedule(result);
    }

    /** 连续两周完成率都低于 50% —— 该下调每周天数重新生成了。 */
    public boolean shouldSuggestReplan(long todayEpochDay) {
        List<Double> finished = new ArrayList<Double>();
        for (int week = 1; week <= 52; week++) {
            long lastDay = -1;
            for (ScheduledSession session : sessions) {
                if (session.week() == week) {
                    lastDay = Math.max(lastDay, session.epochDay());
                }
            }
            if (lastDay < 0) {
                break;
            }
            if (lastDay < todayEpochDay) {
                finished.add(weekCompletion(week, false));
            }
        }
        int size = finished.size();
        return size >= 2
                && finished.get(size - 1) < REPLAN_THRESHOLD
                && finished.get(size - 2) < REPLAN_THRESHOLD;
    }

    /** 该日期所在周的周一。 */
    public static long startOfWeek(long epochDay) {
        LocalDate date = LocalDate.ofEpochDay(epochDay);
        return epochDay - (date.getDayOfWeek().getValue() - 1);
    }
}
