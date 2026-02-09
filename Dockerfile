# Use official AWS Lambda Python base image (matches your Lambda runtime)
FROM public.ecr.aws/lambda/python:3.12

# Set working directory inside container
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy and install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy your application code
COPY app.py .

# The CMD is ignored by Lambda — it uses the handler you specify in AWS console
# But include it for local testing if needed
CMD ["app.handler"]
