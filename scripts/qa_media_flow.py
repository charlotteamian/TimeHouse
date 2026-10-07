#!/usr/bin/env python3
"""Show repaired media through the real Android exercise-detail path, then restore state."""
from pathlib import Path
exec(Path('scripts/qa_routines_flow.py').read_text().split('\nstop()\noriginal =')[0])
stop()
original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    fixture({'version':1,'title':'动作示范检查','intensity':'MEDIUM','reason':'','safety':'','limited':False,'notes':[],'budget':0,'active':False,'items':[{'id':'dataset_1324_0294','sets':2,'reps':'8-12','rpe':'7','rest':60,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}]})
    tap('查看课程 →');tap('看示范与要点')
    check(any('哑铃弯举' in t for t in texts()), 'Repaired exercise opens through actual detail view')
    snapshot('repaired-curl-in-app')
finally:
    write_state(original);launch()
