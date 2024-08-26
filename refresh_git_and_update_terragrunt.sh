echo 'Update Git Repos? y/n'
read updateRepos
echo 'Clean Terragrunt Caches? y/n'
read cleanTerragrunt
echo 'Hard Refresh Every Repo? (del+clone)'
read hardRefreshRepos
export workingPath='<path-to-your-dir' # e.g. /Users/Kurt/code
export codeDir='<name-of-your-code-directory' # e.g. code

if [[ $hardRefreshRepos == y ]]
then

    for dir in ~/${codeDir}/*/
        do
            # TODO make this a list or repos and check if repo is in the list using `contains()`
            if [[ $dir == ${workingPath}repoName1/ || $dir == ${workingPath}repoName2/ ]]
            then
                break
            else
                rm -rf $dir
                git clone git@github.com:<your-GH>/$dir.git
            fi
        done
fi

if [[ $updateRepos == y ]]
then
    for dir in ~/${codeDir}/*/
        do
            # SKIP REPOS LISTED HERE
            # if [[ $dir =~ ${workingPath}repoName1/ ]]
            # then
            #     break
            #     fi
            echo $dir
            cd $dir
            git stash
            git checkout main
            git pull
            git stash pop
            if [[ $cleanTerragrunt == y ]]
            then
                find . -type d -name '.terragrunt-cache' -exec rm -rf {} \;
                find . -type f -name '.terraform.lock.hcl' -exec rm -rf {} \;
                fi
            cd ~/${codeDir}
        done
fi
