from .thread.defining import run_defining_scenario
from .thread.determining import run_determining_scenario
from .thread.subclass import run_subclass_scenario as run_thread_subclass_scenario
from .thread.lock import run_lock_scenario
from .thread.rlock import run_rlock_scenario
from .thread.semaphore import run_semaphore_scenario
from .thread.condition import run_condition_scenario
from .thread.event import run_event_scenario
from .thread.barrier import run_barrier_scenario
from .thread.queue import run_queue_scenario as run_thread_queue_scenario

from .process.spawning import run_spawning_scenario
from .process.naming import run_naming_scenario
from .process.background import run_background_scenario
from .process.killing import run_killing_scenario
from .process.subclass import run_subclass_scenario as run_process_subclass_scenario
from .process.queue import run_queue_scenario as run_process_queue_scenario
from .process.pipes import run_pipes_scenario
from .process.sync import run_sync_scenario
from .process.pool import run_pool_scenario


THREAD_REGISTRY = {
    "defining": run_defining_scenario,
    "determining": run_determining_scenario,
    "subclass": run_thread_subclass_scenario,
    "lock": run_lock_scenario,
    "rlock": run_rlock_scenario,
    "semaphore": run_semaphore_scenario,
    "condition": run_condition_scenario,
    "event": run_event_scenario,
    "barrier": run_barrier_scenario,
    "queue": run_thread_queue_scenario,
}

PROCESS_REGISTRY = {
    "spawning": run_spawning_scenario,
    "naming": run_naming_scenario,
    "background": run_background_scenario,
    "killing": run_killing_scenario,
    "subclass": run_process_subclass_scenario,
    "queue": run_process_queue_scenario,
    "pipes": run_pipes_scenario,
    "sync": run_sync_scenario,
    "pool": run_pool_scenario,
}


def get_registry(method: str):
    registries = {
        "thread": THREAD_REGISTRY,
        "process": PROCESS_REGISTRY
    }
    return registries.get(method)