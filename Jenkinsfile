pipeline {
    agent any
    
    environment {
        PYTHON_PATH = 'C:/Users/maksi/AppData/Local/Programs/Python/Python313/python.exe'
        DJANGO_SETTINGS_MODULE = 'config.settings'
        NODE_DIR = 'G:\\Apps\\AllWithWEB\\nodejs'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Получение кода из репозитория...'
                checkout scm
            }
        }
        
        stage('Backend Setup') {
            steps {
                echo '🐍 Настройка Python окружения...'
                bat "\"${PYTHON_PATH}\" -m venv venv"
                bat "venv\\Scripts\\python.exe -m pip install --upgrade pip"
                bat "venv\\Scripts\\python.exe -m pip install -r requirements.txt"
            }
        }
        
        stage('Database Migration') {
            steps {
                echo '🗄️ Применение миграций базы данных...'
                bat "venv\\Scripts\\python.exe manage.py migrate --noinput"
            }
        }
        
        stage('Seed Database') {
            steps {
                echo '🌱 Генерация тестовых данных в базу...'
                bat "venv\\Scripts\\python.exe manage.py seed_db"
            }
        }
        
        stage('Backend Tests') {
            steps {
                echo '🧪 Запуск тестов Django...'
                bat "venv\\Scripts\\python.exe manage.py test --verbosity=2"
            }
        }
        
        stage('Frontend Setup') {
            steps {
                echo '📦 Установка зависимостей Vue...'
                dir('frontend') {
                    bat "set PATH=${NODE_DIR};%PATH% && npm install"
                }
            }
        }
        
        stage('Frontend Build') {
            steps {
                echo '🏗️ Сборка Vue приложения...'
                dir('frontend') {
                    bat "set PATH=${NODE_DIR};%PATH% && npm run build"
                }
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo '💾 Сохранение артефактов сборки...'
                archiveArtifacts artifacts: 'frontend/dist/**', fingerprint: true
                echo '✅ Сборка успешно завершена!'
            }
        }
    }
    
    post {
        always {
            echo '🏁 Pipeline завершен!'
            bat 'if exist venv rmdir /s /q venv'
        }
        success {
            echo '✅ Все этапы пройдены успешно!'
        }
        failure {
            echo '❌ Ошибка в процессе сборки!'
        }
    }
}