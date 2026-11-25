import json
import logging
from aiokafka import AIOKafkaConsumer
from app.core.config import settings
from app.models.profile import Profile      # <-- Правильный импорт
from app.db.session import SessionLocal     # <-- Импорт сессии

logger = logging.getLogger("uvicorn.error")

async def start_consumer():
    logger.info("Запуск Kafka Consumer...")
    
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKERS,
        group_id=settings.KAFKA_GROUP_ID,
        auto_offset_reset="earliest"
    )

    await consumer.start()
    logger.info("Consumer успешно подключен к Kafka")

    try:
        async for msg in consumer:
            try:
                data = json.loads(msg.value.decode("utf-8"))
                logger.info(f"Получено событие: {data}")
                
                user_id = data.get("user_id")
                email = data.get("email")
                
                if not user_id or not email:
                    logger.warning("В сообщении нет user_id или email, пропускаем")
                    continue

                # Открываем сессию, сохраняем, закрываем
                async with SessionLocal() as session:
                    profile = Profile(
                        user_id=user_id, 
                        display_name=email.split("@")[0]
                    )
                    session.add(profile)
                    await session.commit()
                    logger.info(f"Профиль для {email} сохранен в БД")
                
                await consumer.commit()
                
            except Exception as e:
                logger.error(f"Ошибка при обработке сообщения: {e}")
    finally:
        await consumer.stop()
        logger.info("Consumer остановлен")