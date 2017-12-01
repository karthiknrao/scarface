import subprocess
import time
import datetime
import os
import logging

logging.basicConfig(filename="activity.log", level=logging.INFO)

cmd = [ 'osascript', 'printAppTitle.scpt' ]

blacklistedtasksfile = 'black_list'
tasklistfile = 'task_list'

def parse_taskfile(fname):
    lines = [ x.strip().split() for x in open(fname).readlines() ]
    today = datetime.datetime.now()
    date = today.date()
    strdate = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
    task_lists = []
    for line in lines:
        startts = strdate + ' ' + line[0]
        startts = time.mktime(datetime.datetime.strptime(startts, "%d/%m/%Y %H:%M").timetuple())
        startts = int(startts)
        endts = strdate + ' ' + line[1]
        endts = time.mktime(datetime.datetime.strptime(endts, "%d/%m/%Y %H:%M").timetuple())
        endts = int(endts)
        task = line[2]
        wat = ' '.join(line[3:])
        task_lists.append( ( startts, endts, task, wat ) )
    return task_lists

def parse_blacklistfile(fname):
    return [ x.strip() for x in open(fname).readlines() ]

def get_current_task(task_lists,ts):
    for task in task_lists:
        if ts > task[0] and ts < task[1]:
            return task
    return (None,None,'','')

def process_tasktag(tag):
    if ',' in tag:
        return tag.split(',')
    else:
        return [tag]
    
def check_current_status(window,tags):
    count = 0
    notifywindow = 4
    wlen = len(window)
    tasktag,blacklisttag = tags
    notify = None
    tasktags = process_tasktag(tasktag)

    multitag = []
    for tag_ in tasktags:
        count = 0
        for i in range(notifywindow):
            if tag_.lower() not in window[wlen-1-i].lower():
                count += 1
            if count == 4:
                multitag.append(count)
    if sum(multitag) == len(tasktags)*4:
        return 1, tasktag
    for tag_ in blacklisttag:
        count = 0
        for i in range(notifywindow):
            if tag_.lower() in window[wlen-1-i].lower():
                count += 1
            if count == 4:
                return 2, tag_
    return None

def get_history(window,timewindow):
    logs = [ x.split('\t')[1] for x in window ]
    logs = logs[-timewindow:]
    ulogs = set(logs)
    if len(ulogs) > 4:
        return 3
    
def send_notification(notify,task,app):
    cmd = 'terminal-notifier -title ActivityMonitor -subtitle "URGENT" -message "%s" -appIcon http://www.arrayserver.com/wiki/images/c/cb/Warning.png'
    if notify == 1:
        mess = app + ' ' + task
        cmdf = cmd % mess
        os.system(cmdf)
    if notify == 2:
        mess = 'GET OFF ' + task
        cmdf = cmd % mess
        os.system(cmdf)
    if notify == 3:
        mess = 'Focus MF'
        cmdf =  cmd % mess
        os.system(cmdf)

if __name__ == '__main__':
    task_list = parse_taskfile(tasklistfile)
    blacktask_list = parse_blacklistfile(blacklistedtasksfile)

    logs = []
    while True:
        now = int(time.time())
        datetimestamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
        outval = datetimestamp + '\t' + str(stdout_value)
        
        logs.append(outval)
        logging.info(outval)
        
        task = get_current_task(task_list, now)
        if len(logs) > 10:
            status = check_current_status(logs,(task[3],blacktask_list))
            if status != None:
                send_notification(status[0],status[1],task[2])
        time.sleep(1.0)
    
