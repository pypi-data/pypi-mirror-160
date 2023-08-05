[![NPM version](https://badge.fury.io/js/cdk-gitlab.svg)](https://badge.fury.io/js/cdk-gitlab)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab.svg)](https://badge.fury.io/py/cdk-gitlab)
[![release](https://github.com/pahud/cdk-gitlab/actions/workflows/release.yml/badge.svg)](https://github.com/pahud/cdk-gitlab/actions/workflows/release.yml)

# cdk-gitlab

High level CDK construct to provision GitLab integrations with AWS

# Install

Use the npm dist tag to opt in CDKv1 or CDKv2:

```sh
// for CDKv2
npm install cdk-gitlab
or
npm install cdk-gitlab@latest

// for CDKv1
npm install cdk-gitlab@cdkv1
```

# Sample

```python
import { Provider, FargateJobExecutor, FargateRunner, JobExecutorImage } from 'cdk-gitlab';

const provider = new Provider(stack, 'GitlabProvider', { vpc });

// create a Amazon EKS cluster
provider.createFargateEksCluster(stack, 'GitlabEksCluster', {
  clusterOptions: {
    vpc,
    version: eks.KubernetesVersion.V1_19,
  },
});

// create a default fargate runner with its job executor
provider.createFargateRunner();

// alternatively, create the runner and the executor indivicually.
// first, create the executor
const executor = new FargateJobExecutor(stack, 'JobExecutor', {
  image: JobExecutorImage.DEBIAN,
});

// second, create the runner with the task definition of the executor
new FargateRunner(stack, 'FargateRunner', {
  vpc,
  executor,
});

// TBD - create Amazon EC2 runner for the GitLab
provider.createEc2Runner(...);

});
```

# Fargate Runner with Amazon ECS

On deployment with `createFargateRunner()`, the **Fargate Runner** will be provisioned in Amazon ECS with AWS Fargate and [Amazon ECS Capacity Providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-capacity-providers.html). By default, the `FARGATE` and `FARGATE_SPOT` capacity providers are available for the Amazon ECS cluster and the runner and job executor will run on `FARGATE_SPOT`. You can specify your custom `clusterDefaultCapacityProviderStrategy` and `serviceDefaultCapacityProviderStrategy` properties from the `FargateRunner` construct for different capacity provider strategies.

# Deploy

```sh
cdk deploy -c GITLAB_REGISTRATION_TOKEN=<TOKEN>
```
