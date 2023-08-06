import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-sigv4-request-generator",
    version="0.0.1",
    author="Ivan Sushkov",
    author_email="ivan.sushkov91@gmail.com",
    description="AWS Signature Version 4 signing process (Python)",
    long_description="This package allows you to add the authorization headers to your request required by Amazon's "
                     "signature version 4.",
    long_description_content_type="text/markdown",
    url="https://github.com/ionesu/aws_sigv4_request_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
