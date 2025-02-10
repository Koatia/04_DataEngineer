#!/bin/bash

# Получение имени текущего каталога и формирование имени репозитория
REPO="$(basename "$(pwd)").git"
BRANCH="master"
REMOTE1="origin"
REMOTE2="mirror"
GITHUB_URL="git@github.com:Koatia/$REPO"
GITVERSE_URL="ssh://git@gitverse.ru:2222/Kostia/$REPO"

# Функция для добавления удаленного репозитория, если он не существует
add_remote() {
    if ! git remote | grep -q "$1"; then
        git remote add "$1" "$2"
    fi
}

# Добавление удаленных репозиториев
add_remote $REMOTE1 $GITHUB_URL
add_remote $REMOTE2 $GITVERSE_URL

# Пулл изменений в оба репозитория
commands=(
    "git pull $REMOTE1 $BRANCH"
    "git pull $REMOTE2 $BRANCH"
    "git status"
    "git log --oneline --all --graph"
)

for command in "${commands[@]}"; do
    echo
    echo "*****************************************"
    echo "Выполняется $command"
    eval $command
done

echo '--------'
echo "Обновление завершено"
