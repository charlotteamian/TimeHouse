#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JAVA_HOME="${JAVA_HOME:-/Applications/Android Studio.app/Contents/jbr/Contents/Home}"
JAVAC="$JAVA_HOME/bin/javac"
JAVA="$JAVA_HOME/bin/java"
OUT="$ROOT/build/test-classes"

rm -rf "$OUT"
mkdir -p "$OUT"

"$JAVAC" -encoding UTF-8 -d "$OUT" \
  $(find "$ROOT/app/src/main/java/com/restartday/fitness/domain" "$ROOT/app/src/test/java/com/restartday/fitness/domain" -name '*.java' | sort) \
  "$ROOT/app/src/main/java/com/restartday/fitness/app/GeminiModelName.java" \
  "$ROOT/app/src/main/java/com/restartday/fitness/app/GeminiResponseText.java" \
  "$ROOT/app/src/main/java/com/restartday/fitness/app/GroqEndpoint.java" \
  "$ROOT/app/src/test/java/com/restartday/fitness/app/GeminiModelNameTest.java" \
  "$ROOT/app/src/test/java/com/restartday/fitness/app/GeminiResponseTextTest.java" \
  "$ROOT/app/src/test/java/com/restartday/fitness/app/GroqEndpointTest.java"

"$JAVA" -cp "$OUT" com.restartday.fitness.domain.RecommenderTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.SessionTimeModelTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.ProgramBuilderTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.ProgramScheduleTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.HeartRateStatsTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.AdHocPlannerTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.NutritionPlannerTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.MealDraftTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.DayFoodLogTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.DailyGapTest
"$JAVA" -cp "$OUT" com.restartday.fitness.domain.RecipeSourcesTest
"$JAVA" -cp "$OUT" com.restartday.fitness.app.GeminiModelNameTest
"$JAVA" -cp "$OUT" com.restartday.fitness.app.GeminiResponseTextTest
"$JAVA" -cp "$OUT" com.restartday.fitness.app.GroqEndpointTest
"$ROOT/scripts/validate_exercise_dataset.sh"
python3 "$ROOT/scripts/validate_recipe_dataset.py"
python3 "$ROOT/scripts/generate_voice_cues.py" --check
python3 "$ROOT/scripts/validate_quick_meals.py"
