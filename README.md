# Project goal

This simple project demonstrates the conditional creation of resources using [Pulumi](https://www.pulumi.com/), based on the state of pre-existing resources.

Inspired by [this blog post](https://loige.co/create-resources-conditionally-with-cdk/).

## Setup

First of all clone the repo:

```bash
git clone https://github.com/wtfzambo/pulumi-conditional-resource.git
```

### Creating resources

You will need to create 2 AWS SSM parameters and 1 bucket. Open the AWS console and create the following resources:

- SSM parameter 1: `/pulumiExample/dev/shouldCreateBucket` with value `true`
- SSM parameter 2: `/pulumiExample/prod/shouldCreateBucket` with value `false`
- S3 bucket: `pulumiexample-prod-<YOUR_AWS_ACCOUNT_ID>`

You can quickly retrieve the AWS account ID by running the following command if you have AWS CLI installed:

```bash
aws sts get-caller-identity
```

### Environment

This project uses [named AWS profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) for authentication, so make sure you have the right setup beforehand.

Export the AWS_PROFILE environment variable:

- `export AWS_PROFILE=my_profile` on Mac or Linux
- `$env:AWS_PROFILE=my_profile` on Windows Powershell

### Install pulumi

- `brew install pulumi` on Mac or Linux
- `scoop install pulumi` on Windows

Pulumi can use [different backends](https://www.pulumi.com/docs/intro/concepts/state/) to manage state. For simplicity, let's use a local one.

```bash
pulumi login --local
```

### Install python packages

```bash
python -m venv .venv
source .venv/bin/activate  # (.venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

## Running the project

Pulumi has the concept of [stacks](https://www.pulumi.com/docs/intro/concepts/stack/) which can be compared to development environments.
Select the dev stack: `pulumi stack select dev` and then run:

```bash
pulumi preview
```

This will show you the resources that are about be created. You will notice that in the outputs, the ARN of the bucket is not displayed, showing `output<string>` instead.
This is because the resource doesn't exist yet.

Now run

```bash
pulumi up -y
```

Pulumi has created the resources and the ARN of the bucket is now available in the output.

---

Now select the prod stack: `pulumi stack select prod` and then run the same commands as above.
In this case, you will see that even during `preview`, the ARN of the bucket is available. This is because on the condition we set, the `prod` stack shouldn't create a new bucket, but just reference the already existing one that you created in the first steps.
