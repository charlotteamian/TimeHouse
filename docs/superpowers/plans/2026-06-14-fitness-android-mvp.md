# Fitness Android MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first stable Android MVP from `docs/superpowers/specs/2026-06-14-fitness-app-design.md`.

**Architecture:** Keep the recommendation rules in pure Java domain classes so they can be tested without Android. Build the Android app as a lightweight native Activity on top of that core, with local in-memory demo state for settings, favorites, custom actions, pending shares, and workout records.

**Tech Stack:** Java 21 from Android Studio JBR, Android SDK command-line build tools, native Android Views, plain Java test harness.

---

### Task 1: Recommendation Core

**Files:**
- Test: `app/src/test/java/com/restartday/fitness/domain/RecommenderTest.java`
- Create: `app/src/main/java/com/restartday/fitness/domain/*.java`

- [x] Write failing tests for back-day parsing, pain avoidance, favorites, unverified filtering, and full-body generation.
- [ ] Implement seed exercises and recommendation rules until the tests pass.

### Task 2: Android App Shell

**Files:**
- Create: `app/src/main/AndroidManifest.xml`
- Create: `app/src/main/res/values/*.xml`
- Create: `app/src/main/java/com/restartday/fitness/app/MainActivity.java`

- [ ] Build four bottom navigation areas: training, library, records, settings.
- [ ] Connect training inputs to the recommendation core.
- [ ] Add injury settings, equipment toggles, favorite actions, custom action draft, and pending share inbox.

### Task 3: Direct Android Build

**Files:**
- Create: `scripts/run_domain_tests.sh`
- Create: `scripts/build_android_debug.sh`
- Create: `scripts/debug_android_emulator.sh`

- [ ] Compile and run the pure Java tests using Android Studio JBR.
- [ ] Package a signed debug APK with `aapt2`, `javac`, `d8`, `zipalign`, and `apksigner`.
- [ ] Install and launch on `Medium_Phone_API_36.1` when the emulator is available.

### Task 4: Verification

- [ ] Run domain tests.
- [ ] Build the debug APK.
- [ ] Install and launch on emulator or report the exact blocker.
- [ ] Capture launcher/log evidence and fix any crash or packaging issue.
