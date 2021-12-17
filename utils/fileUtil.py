
def createNewPuzzleInstance(path, fileName, ext, iday = 0):
    import os
    from inspect import getsourcefile

    def copyTemplate(srcName, dst):
        import shutil
        cfd = os.path.abspath(getsourcefile(lambda:0) + '/..')
        srcDir = cfd + '/templates' + srcName
        dstDir = dst
        shutil.copy(srcDir, dstDir)
        print('created new file from template: %s' % (dstDir))

    if not os.path.isdir(path):
        print('creating folder...')
        os.mkdir(path)
        print('created folder: \t%s' % (path))

    dirlist = os.listdir(path)
    dirLen = len([i for i in dirlist if i not in ['__init__.py', '__pycache__']]) + 1
    
    if ext == 'py' and dirLen >= 25:
        print('preventing the creation of puzle instance more than 25 instances.')
        return

    elif fileName == '__init__' and '__init__' not in dirlist:
        if not os.path.exists(path + '/%s.%s' % (fileName, ext)):
            copyTemplate('/template.'+ ext, path + '/%s.%s' % (fileName, ext))
        else:
            pass

    elif fileName == '__init__' and '__init__' in dirlist:
        pass

    else:
        if not os.path.exists(path + '/%s%d.%s' % (fileName, dirLen if not iday else iday, ext)):
            copyTemplate('/template.'+ ext, path + '/%s%d.%s' % (fileName, dirLen, ext))
        else:
            pass

    return


if __name__ == '__main__':
    pass