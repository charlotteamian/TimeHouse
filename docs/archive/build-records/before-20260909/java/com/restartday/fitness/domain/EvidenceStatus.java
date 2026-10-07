package com.restartday.fitness.domain;

public enum EvidenceStatus {
    GUIDELINE_BACKED("guideline_backed", "指南支持"),
    EXPERT_REVIEWED("expert_reviewed", "已审核"),
    DEFAULT_LIBRARY("default_library", "默认动作"),
    USER_UNVERIFIED("user_unverified", "未验证"),
    REJECTED_OR_NEEDS_EDIT("rejected_or_needs_edit", "需编辑");

    private final String key;
    private final String label;

    EvidenceStatus(String key, String label) {
        this.key = key;
        this.label = label;
    }

    public String key() {
        return key;
    }

    public String label() {
        return label;
    }
}
