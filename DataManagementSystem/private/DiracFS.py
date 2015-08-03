#! /usr/bin/env python
#
# Copyright (C) 2014  Xiabo LI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################
# diracfs is a simple file system for manipulation of DIRAC SE contents,  
# based on fuse, origine for private usage. 
# Function details see readme & release note 
#
# Xiabo Li <li.xiabo@gmail.com>
########################################################################
  
import stat, time, random, errno, os, fuse, atexit
from DIRAC.Core.Base import Script
Script.initialize()

#tmpdir = "/tmp/diracfs_"+os.environ['LOGNAME']
tmpdir = os.path.expandvars( '$HOME/.diracfs' )
  
class DiracFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        fuse.fuse_python_api = (0, 2)
        fuse.Fuse.__init__(self, *args, **kw)
        self.tmpdir = tmpdir
        self.SE = "DIRAC-USER"
        self.file = {}
        self.result = {}
        from DIRAC.Core.Security import ProxyInfo
        self.proxy = ProxyInfo.getProxyInfo()

    def getattr(self, path):
        p = os.path.dirname(path)
        from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
        self.result = FileCatalogClient().listDirectory(p,True)
        st = fuse.Stat()
        #print "+++++++++++++++++++++ "+self.SE
        #print p
        #print self.proxy
        #print self.result['Value']['Successful'][p]
        if path=='/':
            st.st_mode = (stat.S_IFDIR | 0755)
            st.st_ino = 0
            st.st_dev = 0
            st.st_nlink = 2
            st.st_uid = os.getuid()
            st.st_gid = os.getgid()
            st.st_size = 4096
            st.st_atime = time.time()
            st.st_mtime = time.time()
            st.st_ctime = time.time()
        elif self.result["OK"] and self.result['Value']['Successful'][p]['Files'].get(path):
            md = self.result['Value']['Successful'][p]['Files'][path]['MetaData']
            st.st_mode = (stat.S_IFREG | md['Mode'])
            st.st_ino = 0
            st.st_dev = 0
            st.st_nlink = 1
            st.st_uid = os.getuid() if md['Owner']==self.proxy['Value']['username'] else 65534
            st.st_gid = os.getgid() if md['OwnerGroup']==self.proxy['Value']['group'] else 65534
            st.st_size = md['Size']
            st.st_atime = time.mktime(md['ModificationDate'].timetuple())
            st.st_mtime = time.mktime(md['ModificationDate'].timetuple())
            st.st_ctime = time.mktime(md['CreationDate'].timetuple())
        elif self.result["OK"] and (self.result['Value']['Successful'][p]['SubDirs'].get('/'+path) or self.result['Value']['Successful'][p]['SubDirs'].get(path)):
            #md = self.result['Value']['Successful'][p]['SubDirs']['/'+path] if p=='/' else self.result['Value']['Successful'][p]['SubDirs'][path]
            # change to DIRAC version v6r12p16
            md = self.result['Value']['Successful'][p]['SubDirs'][path]
            st.st_mode = (stat.S_IFDIR | md['Mode'])
            st.st_ino = 0
            st.st_dev = 0
            st.st_nlink = 2
            st.st_uid = os.getuid() if md['Owner']==self.proxy['Value']['username'] else 65534
            st.st_gid = os.getgid() if md['OwnerGroup']==self.proxy['Value']['group'] else 65534
            st.st_size = 4096
            st.st_atime = time.mktime(md['ModificationDate'].timetuple())
            st.st_mtime = time.mktime(md['ModificationDate'].timetuple())
            st.st_ctime = time.mktime(md['CreationDate'].timetuple())
        else :
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        dirents = [ '.', '..']
        from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
        self.result = FileCatalogClient().listDirectory(path)
        if self.result['OK']:
            dirents.extend(x.split('/')[-1] for x in self.result['Value']['Successful'][path]['Files'].keys())
            dirents.extend(x.split('/')[-1] for x in self.result['Value']['Successful'][path]['SubDirs'].keys())
            for r in dirents:
                yield fuse.Direntry(r)

    def getdir(self, path):
        print '*** getdir', path
        return -errno.ENOSYS

    def mythread ( self ):
        print '*** mythread'
        return -errno.ENOSYS

    def chmod ( self, path, mode ):
        print '*** chmod', path, oct(mode)
        from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI
        from COMDIRAC.Interfaces import DCatalog
        FileCatalogClientCLI( DCatalog().catalog ).do_chmod(str(oct(mode&0777))[1:]+" "+path)
        #return -errno.ENOSYS
        return 0

    def chown ( self, path, uid, gid ):
        print '*** chown', path, uid, gid
        #from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI
        #from COMDIRAC.Interfaces import DCatalog
        #FileCatalogClientCLI( DCatalog().catalog ).do_chown(uid+" "+path)
        #FileCatalogClientCLI( DCatalog().catalog ).do_chgrp(gid+" "+path)
        return -errno.ENOSYS

    def fsync ( self, path, isFsyncFile ):
        print '*** fsync', path, isFsyncFile
        return -errno.ENOSYS

    def link ( self, targetPath, linkPath ):
        print '*** link', targetPath, linkPath
        return -errno.ENOSYS

    def mkdir ( self, path, mode ):
        print '*** mkdir', path, oct(mode)
        from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI
        from COMDIRAC.Interfaces import DCatalog
        FileCatalogClientCLI( DCatalog().catalog ).do_mkdir(path)
        return 0

    def mknod ( self, path, mode, dev ):
        print '*** mknod', path, oct(mode), dev
        return -errno.ENOSYS

    def create (self, path, flags, mode):
        from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI
        from COMDIRAC.Interfaces import DCatalog
        fcc = FileCatalogClientCLI( DCatalog().catalog )
        tmp = str(time.time())+str(random.random())
        f = open(self.tmpdir+'/'+tmp, 'w+b')
        f.write("\0")
        f.close()
        fcc.do_add( path+" "+self.tmpdir+"/"+tmp+" "+self.SE )
        os.remove(self.tmpdir+'/'+tmp)
        self.file[path] = {"handler":os.tmpfile(),"modified":False}#,"mode":os.stat(path)[stat.ST_MODE]}
        self.file[path]["handler"].write("\0")
        return 0

    def open ( self, path, flags ):
        print '*** open', path, flags
        from DIRAC.DataManagementSystem.Client.DataManager import DataManager
        result = DataManager().getFile( path, destinationDir = self.tmpdir )
        if result["OK"]:
            self.file[path] = {"handler":os.tmpfile(),"modified":False}#,"mode":os.stat(path)[stat.ST_MODE]}
            self.file[path]["handler"].write(open(result["Value"]["Successful"][path],'rb').read())
            os.remove(result["Value"]["Successful"][path])
            return 0
        else:
            return -errno.ENOENT

    def read ( self, path, length, offset ):
        print '*** read', path, length, offset
        self.file[path]["handler"].seek(offset)
        data = self.file[path]["handler"].read(length)
        return data

    def readlink ( self, path ):
        print '*** readlink', path
        return -errno.ENOSYS

    def release ( self, path, flags ):
        print '*** release', path, flags
        #if self.file[path]["mode"]&(stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH):
        #    return -errno.EACCES
        #print self.file[path]
        if self.file[path]["modified"]:
            self.file[path]["handler"].seek(0)
            off = 1 if self.file[path]["handler"].read(1) == '\0' else 0

            tmp = str(time.time())+str(random.random())
            f = open(self.tmpdir+'/'+tmp,"w+b")
            self.file[path]["handler"].seek(off)
            f.write(self.file[path]["handler"].read())
            f.close()
    
            from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI
            from COMDIRAC.Interfaces import DCatalog
            fcc = FileCatalogClientCLI( DCatalog().catalog )
            fcc.do_rm(path)
            fcc.do_add( path+" "+self.tmpdir+"/"+tmp+" "+self.SE )
            os.remove(self.tmpdir+'/'+tmp)
        self.file[path]["handler"].close()
        del self.file[path]
        return 0
        #return -errno.ENOSYS

    def rename ( self, oldPath, newPath ):
        print '*** rename', oldPath, newPath
        return -errno.ENOSYS
        #from DIRAC.DataManagementSystem.Client.ReplicaManager import ReplicaManager
        #from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI
        #from COMDIRAC.Interfaces import DCatalog
        #fcc = FileCatalogClientCLI( DCatalog().catalog )
        #result = ReplicaManager().getFile( oldPath, destinationDir = self.tmpdir )
        #fcc.do_rm(oldPath)
        #fcc.do_add( newPath+" "+self.tmpdir+"/"+oldPath.split('/')[-1]+" "+self.SE )
        #os.remove(self.tmpdir+'/'+oldPath.split('/')[-1])

        #import shutil
        #tmp = str(time.time())+str(random.random())
        #os.mkdir(self.tmpdir+"/"+tmp)
        #shutil.rename(oldPath, self.tmpdir+"/"+tmp)
        #dstdir =  os.path.join(newPath, os.path.dirname(oldPath))
        #os.makedirs(dstdir)
        #shutil.copytree(oldPath, newPath)
        #shutil.rmtree(oldPath)
        #os.rmdir(oldPath)
        #time.sleep(5)
        #os.rename(oldPath, self.tmpdir+"/"+oldPath)
        #os.rename(self.tmpdir+"/"+oldPath, newPath)
        #os.rmdir(self.tmpdir+"/"+oldPath)
        #return 0

    def rmdir ( self, path ):
        print '*** rmdir', path
        from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI
        from COMDIRAC.Interfaces import DCatalog
        FileCatalogClientCLI( DCatalog().catalog ).do_rmdir(path)
        return 0

    def statfs ( self ):
        print '*** statfs'
        #return -errno.ENOSYS
        return 0

    def symlink ( self, targetPath, linkPath ):
        print '*** symlink', targetPath, linkPath
        return -errno.ENOSYS

    def truncate ( self, path, size ):
        print '*** truncate', path, size
        #if self.file[path]["mode"]&(stat.S_IWUSR)==0:#|stat.S_IRGRP|stat.S_IROTH)==0:
        #    return -errno.EACCES
        self.file[path]["handler"].seek(0)
        self.file[path]["handler"].truncate(size)
        self.file[path]["modified"] = True
        return 0

    def unlink ( self, path ):
        print '*** unlink', path
        from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI
        from COMDIRAC.Interfaces import DCatalog
        fcc = FileCatalogClientCLI( DCatalog().catalog )
        fcc.do_rm(path)
        return 0

    def utime ( self, path, times ):
        print '*** utime', path, times
        return -errno.ENOSYS

    def write ( self, path, buf, offset ):
        print '*** write', path, buf, offset
        #print self.file[path]
        #if self.file[path]["mode"]&(stat.S_IWUSR)==0:#|stat.S_IRGRP|stat.S_IROTH)==0:
        #    return -errno.EACCES
        self.file[path]["handler"].seek(offset)
        self.file[path]["handler"].write(buf)
        self.file[path]["modified"] = True
        return len(buf)

    #def access(self, path, mode):
    #    if not os.access(path, mode):
    #        return -errno.EACCES


def main(args):
    usage="""
        DiracFS: A filesystem to allow viewing dirac cloud filesystem.
    """ + fuse.Fuse.fusage
    if not os.path.isdir(tmpdir):
        os.makedirs(tmpdir)
    server = DiracFS(version="%prog " + fuse.__version__,
                    usage=usage, dash_s_do='setsingle')
    #server.fuse_args.add('allow_other')
    server.parser.add_option(mountopt="SE", metavar="Storage Element ID", default="DIRAC-USER", help="specify the used storage element [default: %default]")
    server.parse(values = server,errex=1)
#    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    import sys
    main(sys.argv)


@atexit.register
def goodbye():
  import shutil
  shutil.rmtree(tmpdir)
  #os.rmdir(tmpdir)
