pipeline {
    agent any
    
    environment {
        // Переменные окружения
        PYTHON_VENV = 'venv'
        DJANGO_SETTINGS_MODULE = 'config.settings'
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
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate && pip install --upgrade pip'
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }
        
        stage('Database Migration') {
            steps {
                echo '🗄️ Применение миграций базы данных...'
                bat 'venv\\Scripts\\activate && python manage.py migrate --noinput'
            }
        }
        
        stage('Backend Tests') {
            steps {
                echo '🧪 Запуск тестов Django...'
                bat 'venv\\Scripts\\activate && python manage.py test --verbosity=2'
            }
        }
        
        stage('Frontend Setup') {
            steps {
                echo '📦 Установка зависимостей Vue...'
                dir('frontend') {
                    bat 'npm install'
                }
            }
        }
        
        stage('Frontend Build') {
            steps {
                echo '🏗️ Сборка Vue приложения...'
                dir('frontend') {
                    bat 'npm run build'
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
            // Очистка виртуального окружения (опционально)
            bat 'if exist venv rmdir /s /q venv'
        }
        success {
            echo '✅ Все этапы пройдены успешно!'
        }
        failure {
            echo '❌ Ошибка в процессе сборки!'
        }
        unstable {
            echo '⚠️ Сборка завершена с предупреждениями!'
        }
    }
}