#!/bin/bash

REQ_FILES=(
  "/code/requirements"
)

for f in "${REQ_FILES[@]}"; do
  rm ${f}.txt & pip-compile --generate-hashes -o ${f}.txt ${f}.in || exit 1;
done
