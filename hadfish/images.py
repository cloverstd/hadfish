#!/usr/bin/env python
# -*- coding: utf-8 -*-
import qiniu.conf
import qiniu.io
import qiniu.rs
from cStringIO import StringIO

qiniu.conf.ACCESS_KEY = "mTjx-jhzEBaeRpY60t--XLCVdKWDopZK4TqIRPDj"
qiniu.conf.SECRET_KEY = "93nRC4uy98qJSCsadtz7-HLPCiF95-qyZDmajtGC"


def upload_images(bucket, filename, stream):
    policy = qiniu.rs.PutPolicy("%s:%s" % (bucket, filename))
    uptoken = policy.token()
    # extra = qiniu.io.PutExtra()
    # extra.mime_type = "text/plain"
    ret, err = qiniu.io.put(uptoken, filename, stream)
    if err:
        return False
    return True


def delete_images(bucket, filename):
    path = list()
    if isinstance(filename, list):
        for f in filename:
            path.append(qiniu.rs.EntryPath(bucket, f))
        rets, err = qiniu.rs.Client().batch_delete(path)
        if not [ret["code"] for ret in rets] == [200, 200]:
            return False
    else:
        ret, err = qiniu.rs.Client().delete(bucket, filename)
        if err:
            return False
    return True

if __name__ == "__main__":
    data = StringIO("hello!aaaaaaaaa")
    # print upload_images("hadfish", "test.txt", data)
    # print upload_images("hadfish", "test2.txt", data)
    # print delete_images("hadfish", ["test.txt", "test2.txt"])
