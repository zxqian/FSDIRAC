# FSDIRAC
This is a project to add a file system functionality to DIRAC to access grid files as if they are local.<p>
This simple file system is based on fuse, origine for private usage.

### Environment requirement :
*  python : 2.6, 2.7
*  fuse installed : install python fuse (linux fuse.py; mac OSXFUSE & fuse.py) manually

### To allow user to mount diracfs on linux, two different methods can be used (both needs administration privilege):
*  add user to fuse group
*  insert 'user_allow_other' into /etc/fuse.conf and do 'chmod o+x /bin/fusermount'

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

### Commands (tested) available :  
```
  mkdir [-p]  
  rmdir  
  rm [-rf]  
  cp [-r]  
  ls [-lha -R]  
  cat  
  less  
  more  
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
  mv : dirac FileCatalogue does not support move procedure. Can be done 
       by copy to local then send back to remote dirac SE 
```

### Troubleshooting :

* The execution time of command depends on the charge of DIRAC Storage Element, some commands as 'rm' et 'cp' can take long time. Sometime after copy file to DIRAC, command 'ls' does not show correct listing immediately.


