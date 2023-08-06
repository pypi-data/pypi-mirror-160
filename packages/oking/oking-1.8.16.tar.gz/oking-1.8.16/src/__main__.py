import src
from time import sleep
import schedule
import logging
from src.jobs import products_jobs, system_jobs, client_jobs
from src.jobs import stock_jobs
from src.jobs import price_jobs
from src.jobs import order_jobs
from src.api import oking
from src.jobs.system_jobs import OnlineLogger

logger = logging.getLogger()
send_log = OnlineLogger.send_log


# region Estoques

def instantiate_insert_stock_semaphore_job(job_config: dict) -> None:
    """
    Instancia o job de inserção/atualização de estoques na tabela de semáforo
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    stock_jobs.job_insert_stock_semaphore(job_config)


def instantiate_send_stock_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos estoques para a api okVendas
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    stock_jobs.job_send_stocks(job_config)


def instantiate_send_ud_stock_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos estoques por Unidades de distribuição para a api okVendas
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    stock_jobs.job_send_stocks_ud(job_config)


# endregion Estoques


# region Precos

def instantiate_insert_price_semaphore_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos preços para o banco semáforo

    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    price_jobs.job_insert_prices_semaphore(job_config)


def instantiate_send_price_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos preços para a api okVendas

    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    price_jobs.job_send_prices(job_config)


def instantiate_prices_list_job(job_config: dict) -> None:
    """
    Instancia o job de envio das listas de preço para o banco semáforo

    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    price_jobs.job_prices_list(job_config)


def instantiate_product_prices_list_job(job_config: dict) -> None:
    """
    Instancia o job dos produtos das listas de preço

    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    price_jobs.job_products_prices_list(job_config)

# endregion Precos


# region Produtos

def instantiate_insert_products_semaphore_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos produtos para o banco semáforo
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    products_jobs.job_insert_products_semaphore(job_config)


def instantiate_update_products_semaphore_job(job_config: dict) -> None:
    """
    Instancia o job de atualização dos produtos no banco semáforo
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    products_jobs.job_update_products_semaphore(job_config)


def instantiate_send_products_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos produtos para a api okVendas
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    products_jobs.job_send_products(job_config)


# endregion Produtos


# region Pedidos

def instantiate_orders_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos pedidos para o ERP, incluindo pedidos ainda não pagos
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    order_jobs.define_job_start(job_config)


def instantiate_paid_orders_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos pedidos pagos para o ERP
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    order_jobs.define_job_start(job_config)


def instantiate_b2b_orders_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos pedidos B2B para o ERP, incluindo pedidos ainda não pagos
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    order_jobs.define_job_start(job_config)


def instantiate_paid_b2b_orders_job(job_config: dict) -> None:
    """
    Instancia o job de envio dos pedidos pagos B2B para o ERP
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    order_jobs.define_job_start(job_config)


def instantiate_invoice_job(job_config: dict) -> None:
    """
    Intancia o job de envio das NFs de pedidos para a api okvendas
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    order_jobs.job_invoice_orders(job_config)


def instantiate_erp_tracking_job(job_config: dict) -> None:
    """
    Intancia o job de envio do rastreio de pedidos para a api okvendas
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    order_jobs.job_send_erp_tracking(job_config)

# endregion Pedidos


# region Clientes

def instantiate_client_b2b_integration_job(job_config: dict) -> None:
    """
    Instancia o job de envio de clientes para a api okvendas
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    client_jobs.job_send_clients(job_config)


def instantiate_client_integration_job(job_config: dict) -> None:
    """
    Instancia o job de envio de clientes para a api okvendas
    Args:
        job_config: Configuração do job obtida na api do oking
    """
    logger.warning(job_config.get('job_name') + ' | Job nao implementado!')

# endregion Clientes


def instantiate_periodic_execution_notification(job_config: dict) -> None:
    """
    Instancia o job que realiza a notificacao de execucao da integracao para a api okvendas
    Args:
        job_config: Configuração do job
    """
    logger.info(job_config.get('job_name') + ' | Iniciando execucao')
    system_jobs.send_execution_notification(job_config)


# region ConfigJobs

def schedule_job(job_config: dict, time_unit: str, time: int) -> None:
    logger.info(f'Adicionando job {job_config.get("job_name")} ao schedule de {time} em {time} {time_unit}')
    func = get_job_from_name(job_config.get('job_name'))
    if time_unit == 'M':  # Minutos
        schedule.every(time).minutes.do(func, job_config)
    elif time_unit == 'H':  # Horas
        schedule.every(time).hours.do(func, job_config)
    elif time_unit == 'D':  # Dias
        schedule.every(time).days.do(func, job_config)


def get_job_from_name(job_name: str):

    # Estoque
    if job_name == 'insere_estoque_produto_semaforo_job':
        return instantiate_insert_stock_semaphore_job
    elif job_name == 'envia_estoque_produtos_job':
        return instantiate_send_stock_job
    elif job_name == 'envia_estoque_produtos_ud_job':
        return instantiate_send_ud_stock_job

    # Preco
    elif job_name == 'insere_preco_produto_semaforo_job':
        return instantiate_insert_price_semaphore_job

    elif job_name == 'envia_preco_produtos_job':
        return instantiate_send_price_job

    elif job_name == 'lista_preco_job':
        return instantiate_prices_list_job

    elif job_name == 'produto_lista_preco_job':
        return instantiate_product_prices_list_job

    # Catalogacao
    elif job_name == 'envia_catalogo_produto_semaforo_job':
        return instantiate_insert_products_semaphore_job
    elif job_name == 'envia_catalogo_produto_loja_job':
        return instantiate_send_products_job

    # Pedidos
    elif job_name == 'internaliza_pedidos_job':
        return instantiate_orders_job
    elif job_name == 'internaliza_pedidos_pagos_job':
        return instantiate_paid_orders_job
    elif job_name == 'internaliza_pedidos_b2b_job':
        return instantiate_b2b_orders_job
    elif job_name == 'internaliza_pedidos_pagos_b2b_job':
        return instantiate_paid_b2b_orders_job
    elif job_name == 'envia_nota_loja_job':
        return instantiate_invoice_job
    elif job_name == 'envia_rastreio_pedido_job':
        return instantiate_erp_tracking_job

    # Clientes
    elif job_name == 'integra_cliente_b2b_job':
        return instantiate_client_b2b_integration_job
    elif job_name == 'integra_cliente_job':
        return instantiate_client_integration_job

    # Notificacao
    elif job_name == 'periodic_execution_notification':
        return instantiate_periodic_execution_notification

# endregion ConfigJobs


modules: list = [oking.Module(**m) for m in src.client_data.get('modulos')]
assert modules is not None, 'Nao foi possivel obter os modulos da integracao. Por favor, entre em contato com o suporte.'
for module in modules:
    schedule_job({
        'db_host': src.client_data.get('host'),
        'db_port': src.client_data.get('port'),
        'db_user': src.client_data.get('user'),
        'db_type': src.client_data.get('db_type'),
        'db_name': src.client_data.get('database'),
        'db_pwd': src.client_data.get('password'),
        'db_client': src.client_data.get('diretorio_client'),
        'send_logs': module.send_logs,
        'job_name': module.job_name,
        'sql': module.sql
    }, module.time_unit, module.time)

# Job para notificar execucao periodica do Oking a cada 30 min
schedule_job({
    'job_name': 'periodic_execution_notification',
    'execution_start_time': src.start_time,
    'job_qty': len(schedule.get_jobs()),
    'integration_id': src.client_data.get('integracao_id')
}, 'M', 30)


def main():
    logger.info('Iniciando oking __main__')
    while True:
        try:
            schedule.run_pending()
            sleep(5)
        except Exception as e:
            logger.error(f'Erro não tratado capturado: {str(e)}')
            send_log('__main__', src.client_data.get('enviar_logs'), False, f'', 'error', '')


if __name__ == "__main__":
    main()
