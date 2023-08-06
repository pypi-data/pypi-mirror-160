import boto3
from botocore import paginate


class MyFile:
    content = None
    def write(self, data: bytes):
        self.content = data

class AwsSDK:

    def __init__(self, res_name='s3', region_name='cn-north-1', bucket_name='spider-file'):
        self._res_name = res_name
        self.s3 = boto3.resource(res_name, region_name)
        self.s3Client = boto3.client(res_name, region_name)
        self.bucket_name = bucket_name



    @property
    def resName(self):
        return self._res_name

    def getBuckets(self):

        return [bucket.name for bucket in self.s3.buckets.all()]

    def uploadStream(self, k, stream, dir_name=None):
        # Upload a new file
        res = self.s3.Bucket('spider-file').put_object(Key=f"{dir_name}/{k}" if dir_name else k, Body=stream)
        print(res)

    def uploadFile(self, file_name, dir_name='wanfang'):
        with open(file_name, 'rb') as fr:
            self.uploadStream(f"{dir_name}/{file_name}", fr)


    def getDirs(self, bucket_name=None):
        paginator = self.s3Client.get_paginator('list_objects')
        result: paginate.PageIterator = paginator.paginate(Bucket=bucket_name or self.bucket_name, Delimiter='/')
        return [prefix.get('Prefix') for prefix in result.search('CommonPrefixes')]


    def getObjectContent(self, key, bucket_name='spider-file'):
        file = MyFile()
        obj = self.s3.Object(bucket_name, key)
        obj.download_fileobj(file)
        res = file.content.decode()
        # print(res)
        return res









if __name__ == '__main__':
    s3Client = AwsSDK()
    # s3Client.getBuckets()
    # s3Client.uploadFile()
    s3Client.getObjectContent('wanfang/BodyParser.py')



