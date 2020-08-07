# deploy test

### Download packages:
```python
# download packages from ftp server to local path.
python /home/deploytest/deploy/Download_Package.py test_e1.tar /home/deploytest/local/ 001 test_e1_20200729001 192.168.137.82:21:ftpuser1:123456:/devops/
```

### Backup directory:
```python
# backup a directory from source path to backup path.
python /home/deploytest/deploy/Backup_Directory.py /home/deploytest/backup/ /home/deploytest/update/ exclude_dir1,exclude_dir2,efile1,efile2
```

### Update program:
```python
# update program files to update path.
python /home/deploytest/deploy/Update_Program.py /home/deploytest/local/test_e1_20200730001/ /home/deploytest/update/ test_e1.tar APP 192.168.137.82:21:ftpuser1:123456:/devops/
```

### Technical check:

```python
# check process port url
python /home/deploytest/deploy/Technical_Check.py process#ssh,python port#22,3306 url#https://www.baidu.com/,https://cn.bing.com/
```

### Backup program:

```python
# Backup program's files which will be update.
 python /home/deploytest/deploy/Backup_Program.py /home/deploytest/local/test_e2_20200730001/ /home/deploytest/update/ /home/deploytest/backup/ test_e2.tar APP
 ```

### Update common:

```python
# Update program files from common file to updatepath.
python /home/deploytest/deploy/Update_Common.py /home/deploytest/local/test_e3_20200807001/ /home/deploytest/update/dev/ test_e3.tar APP dev 192.168.137.82:21:ftpuser1:123456:/devops/
```

### Backup common:

```python
# Backup program files which will be update.
python /home/deploytest/deploy/Backup_Common.py /home/deploytest/local/test_e3_20200807001/ /home/deploytest/update/dev/ /home/deploytest/backup/ test_e3.tar APP dev
```