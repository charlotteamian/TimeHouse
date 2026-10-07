package com.restartday.fitness.domain;

import java.util.Arrays;
import java.util.List;

/** Shared, deterministic exercise roles. Equipment is a preference only after safety filtering. */
public final class TrainingSelection {
    private TrainingSelection() {}

    public static boolean loaded(Exercise e) {
        if (e.equipment().contains("自重")) return false;
        for (String equipment : e.equipment()) {
            if (!equipment.equals("自重") && !equipment.equals("未标注")) return true;
        }
        return false;
    }

    public static boolean foundation(Exercise e) {
        return Arrays.asList("exercise_bird_dog", "exercise_dead_bug", "exercise_glute_bridge",
                "exercise_wall_pushup", "exercise_sit_to_stand", "exercise_band_external_rotation",
                "exercise_face_pull").contains(e.id());
    }

    public static int preference(Exercise e, Intensity intensity) {
        if (intensity == Intensity.LOW) return foundation(e) ? 15 : 0;
        int score = loaded(e) ? 38 : 0;
        if (foundation(e)) score -= 65;
        // Imported category tags alone cannot identify compound exercise mechanics.
        if (e.evidenceStatus() == EvidenceStatus.GUIDELINE_BACKED) score += 20;
        return score;
    }

    public static boolean matches(Exercise e, String slot) {
        if (slot.equals("拉") && !e.targetRegions().contains("背")) return false;
        if (slot.equals("推") && !e.targetRegions().contains("胸") && !e.targetRegions().contains("肩")) return false;
        if (slot.equals("核心")) return e.targetRegions().contains("核心");
        return e.movementPatterns().contains(slot);
    }

    public static String role(Exercise e) {
        for (String slot : Arrays.asList("髋铰链", "蹲", "推", "拉", "核心", "有氧")) {
            if (matches(e, slot)) return slot;
        }
        String fallback = e.movementPatterns().isEmpty() ? "辅助" : e.movementPatterns().get(0);
        return fallback.equals("拉") || fallback.equals("推") ? "手臂辅助" : fallback;
    }

    public static boolean sameRole(Exercise a, Exercise b) {
        return role(a).equals(role(b));
    }
}
