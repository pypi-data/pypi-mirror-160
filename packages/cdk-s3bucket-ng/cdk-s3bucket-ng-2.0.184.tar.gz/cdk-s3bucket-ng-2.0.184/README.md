[![NPM version](https://badge.fury.io/js/cdk-s3bucket-ng.svg)](https://badge.fury.io/js/cdk-s3bucket-ng)
[![PyPI version](https://badge.fury.io/py/cdk-s3bucket-ng.svg)](https://badge.fury.io/py/cdk-s3bucket-ng)
![Release](https://github.com/neilkuan/cdk-s3bucket/workflows/release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-s3bucket-ng?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-s3bucket-ng?label=pypi&color=blue)

# cdk-s3bucket-ng

cdk-s3bucket-ng is an AWS CDK construct library that provides a drop-in replacement for the Bucket construct with the capability to remove non-empty S3 buckets.

## Install

```bash
Use the npm dist tag to opt in CDKv1 or CDKv2:

// for CDKv2
npm install cdk-s3bucket-ng
or
npm install cdk-s3bucket-ng@latest

// for CDKv1
npm install cdk-s3bucket-ng@cdkv1
```

💡💡💡 please click [here](https://github.com/neilkuan/cdk-s3bucket/tree/cdkv1#readme), if you are using aws-cdk v1.x.x version.💡💡💡

# Why

Sometime we just do some lab , create a S3 Bucket.
Want to destroy resource , after Lab finished.
But We forget delete Object in S3 Bucket first , so destroy will fail.

`cdk-s3bucket-ng`  can help delete object when cdk destroy , just add `removalPolicy: RemovalPolicy.DESTROY`  property .

You never have to delete objects yourself, and the usage is almost the same as the native @aws-cdk/aws-s3.Bucket

## Now Try It !!!

# Sample

```python
import { App, Stack, CfnOutput, RemovalPolicy }  from 'aws-cdk-lib';
import { BucketNg } from 'cdk-s3bucket-ng';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';

// Create a S3 , add props "removalPolicy: RemovalPolicy.DESTROY".
const bucket = new BucketNg(stack, 'Bucket',{
  removalPolicy: RemovalPolicy.DESTROY,
});

//Upload temp file .
new s3deploy.BucketDeployment(stack, 'addResource', {
    sources: [s3deploy.Source.asset('./testdir')],
    destinationBucket: bucket,
  });
// Get S3 Resource via bucket.s3Bucket ...
new CfnOutput(stack, 'BucketName', { value: bucket.bucketName });
```

```bash
# create temp file .
mkdir ./testdir
touch ./testdir/{a.txt,b.txt,c.txt}
ls ./testdir
a.txt  b.txt  c.txt
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
# will delete object in S3 , and delete S3 Bucket
cdk destroy
```

## :clap:  Supporters

[![Stargazers repo roster for @neilkuan/cdk-s3bucket](https://reporoster.com/stars/neilkuan/cdk-s3bucket)](https://github.com/neilkuan/cdk-s3bucket/stargazers)
