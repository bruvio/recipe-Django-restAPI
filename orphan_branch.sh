 #!/bin/bash
 git checkout --orphan Develop

 git status
 git commit -am "Initial commit"
 git branch -D develop
 git branch -m develop
 git push -f origin develop
 git checkout main
