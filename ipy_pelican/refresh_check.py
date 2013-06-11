#!/usr/bin/env python
"""
    Purpose of this hook is to prevent committing files that have refresh:True. 
    Anything committed should be static and locked in once comitted.
"""
import os, sys
import re
import functools

def hg_hook(difflines, line_check):
    linenum, header = 0, False

    filename = None
    for line in difflines: 
        if header:
            # remember the name of the file that this diff affects
            m = re.match(r'(?:---|\+\+\+) ([^\t]+)', line)
            if m and m.group(1) != '/dev/null':
                filename = m.group(1).split('/', 1)[-1]
            if line.startswith('+++ '):
                header = False
            continue

        if line.startswith('diff '):
            header = True
            continue
         # hunk header - save the line number
        m = re.match(r'@@ -\d+,\d+ \+(\d+),', line)
        if m:
            linenum = int(m.group(1))
            continue

        if line.startswith('+') and line_check(line):
            yield filename, linenum

        if line and line[0] in ' +':
            linenum += 1

def _check_refresh(line):
    in_line = 'refresh:True' in line
    return in_line

check_refresh = functools.partial(hg_hook, line_check=_check_refresh)

def check_refresh_hook(ui, repo, **kwargs):
    """
    Mercurial in-process hook
    """
    # hg export tip is supposed to show tip as if
    # commit went through but doesn't seem to work
    # for in process hook. Using hg diff instead
    tip_data = list(os.popen('hg diff'))
    added = 0
    for filename, linenum in check_refresh(tip_data):
        ui.warn('%s, line %d: refresh:True found' %
                              (filename, linenum))
        added += 1
    # hooks return True for error
    if added:
        return True
    return False

if __name__ == '__main__':
    tip_data = os.popen('hg export tip')
    added = 0
    for filename, linenum in check_refresh(tip_data):
        print >> sys.stderr, ('%s, line %d: refresh:True found' %
                              (filename, linenum))
        added += 1
    if added:
        # save the commit message so we don't need to retype it
        os.system('hg tip --template "{desc}" > .hg/commit.save')
        print >> sys.stderr, 'commit message saved to .hg/commit.save'
        sys.exit(1)
