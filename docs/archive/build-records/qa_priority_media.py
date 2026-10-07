from pathlib import Path
exec(Path('scripts/qa_routines_flow.py').read_text().split('\nstop()\noriginal =')[0])
stop()
original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    for xid,label in [('0808','悬挂划船'),('2138','固定自行车')]:
        fixture({'version':1,'title':'新动作示范','intensity':'MEDIUM','reason':'','safety':'','limited':False,'notes':[],'budget':0,'active':False,'items':[{'id':'dataset_1324_'+xid,'sets':1,'reps':'12','rpe':'','rest':30,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}]})
        tap('查看课程 →');tap('看示范与要点')
        check(any(label in t for t in texts()), 'New '+xid+' media opens in actual exercise view')
        snapshot('new-'+xid+'-in-app')
finally:
    write_state(original);launch()
