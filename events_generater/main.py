from etl.base_etl import Etl

if __name__ == "__main__":
    with Etl() as etl:
        for raws in etl.extract.read_db(
            query="select * from notification_database.public.schedule", batch_size=10
        ):
            data_schedulers = etl.transform.convert_shcedule(raws)
            id_schedule = etl.transform.compare_shcedule(data_schedulers)
            if id_schedule:
                for data in etl.extract.read_db(
                    query=f"select * from notification_database.public.events where id in ('{','.join(id_schedule)}')",
                    batch_size=10,
                ):
                    # TODO 1. валидация данных 2. отправка данных на api
                    todo = 325
