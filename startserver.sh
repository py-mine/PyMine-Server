#!/bin/bash
for command in pypy python python3.9 python3.8 python3.7 python3  
do

currentver=$($command -c "import platform;print(platform.python_version())")
requiredver="3.7.9"
if [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then 
        echo "python version ok ($currentver)"
        $command pymine
        exit 0
fi

done

echo "Couldn't find suitable Python version. Please use your package manager to install python 3.7.9 or later"
exit 1
