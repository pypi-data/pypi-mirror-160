import boto3


def is_resource(the_arn: str):
    """
    is the ARN is a secret manager resource?

    :param str the_arn: the ARN
    :return: is the ARN is a secret manager resource?
    :rtype: bool
    """

    # arn:aws:secretsmanager:ap-northeast-1:038528481894:secret:ep/ECS-secret/test-XlIeIr
    return the_arn.startswith("arn:aws:secretsmanager:")


def is_reference_existed(reference_arn: str):
    """
    is reference existed?

    :param str reference_arn: reference ARN
    :return: is reference existed?
    :rtype: bool
    """

    client = boto3.client('secretsmanager')
    secrets = client.list_secrets()["SecretList"]
    return reference_arn in [secret["ARN"] for secret in secrets]
