#!/bin/bash
for command in pypy python python3.9 python3.8 python3.7 python3  
do

#!/bin/bash
currentver=$($command -c "import platform;print(platform.python_version())")
# echo $currentver
requiredver="3.7"
 if [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then 
        echo "python version ok ($currentver)"
        $command pymine
        exit 0
 fi
done

echo Couldnt find Suitble python version. please use your package manager to install python 3.7 or later 
exit 1
