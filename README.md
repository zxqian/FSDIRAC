# FSDIRAC
This is a project to add a file system functionality to DIRAC to access grid files as if they are local.<p>
This simple file system is based on fuse, origine for private usage.

### Environment requirement :
*  python : 2.6, 2.7
*  fuse installed : install python fuse (linux fuse.py; mac OSXFUSE & fuse.py) manually

### To allow user to mount diracfs, two different methods can be used :
*  root adds user to fuse group
*  root does 'chmod +x /bin/fusermount'

### User mount/umount diracfs :
* mount (ex. mount to /tmp/dfs)
```
  mkdir /tmp/dfs 
  dirac-mount.py /tmp/dfs
  dirac-mount.py /tmp/dfs --se=IN2P3-disk  ===> use IN2P3-disk instead of DIRAC-USER
  dirac-mount.py -d /tmp/dfs               ===> turn fuse to debug mode
```
* umount
```
  fusermount -u /tmp/dfs
```

### Commands available :  
```
  mkdir [-p]  
  rmdir  
  rm [-rf]  
  cp [-r]  
  ls [-lha -R]  
  cat  
  less  
  more  
  tail  
  echo >  >>  
  du [-sh]  
  find -name -print 
  rsync
  chmod [-R] 
  tar [tzf] [tjf]
  stat
  xpdf  
  eog
  nano
  vi(vim, gvim) : work although better to set swap file/directory to local 
                  path  
  emacs : work as vi
  mv : - globaly works for files, for directory better to copy to local then  
         copy to remote path and delete local copy (fuse/fuse-python bug?)  
       - cannot overwrite existing file in same directory : dirac GUID ?
```
