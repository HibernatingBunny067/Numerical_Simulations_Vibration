import numpy as np
from typing import Union,Callable,Dict,Optional,List
from numpy.typing import NDArray
from core.integrator import integrate_core
from core.sampling import interpolated_results
from core.output import rk45Output

def __auto_h0__(
        f:Callable,
        t_span:NDArray,
        y0:NDArray,
        rtol:float,
        atol:float,
        sys_params:Optional[NDArray] = None
) -> float:
    t0,tf = t_span[0],t_span[-1]
    f0 = f(t0,y0,sys_params)
    h0:float = 0.0
    scale = atol + rtol*np.abs(y0)
    d0,d1 = np.linalg.norm(y0/scale),np.linalg.norm(f0/scale)

    if d0 < 1e-8 or d1 < 1e-8:
        h0 = 1e-4
    else:
        h0 = float(0.05 * d0 / d1)

    return np.clip(h0,1e-6,(tf-t0)/10)

def __auto_n__(
        ts:NDArray,
        t_span:NDArray,
        rtol:float
) -> int:
    
    t0,tf = t_span[0],t_span[-1]

    if len(ts) > 1:
        dt_min = np.min(np.diff(ts))
        n = int((tf-t0) / dt_min)
        return int(1.5*n)
    else:
        return int((tf-t0)/np.sqrt(rtol))


def rk45(
        f:Callable,
        y0:Union[List,NDArray],
        t_span: Union[List,NDArray],
        h0:Optional[float] = None,
        n:Optional[int] = None,
        rtol:float = 1e-6,
        atol:float = 1e-9,
        t_eval:Optional[NDArray] = None,
        events:Optional[List[Callable]] = None,
        sys_params:Optional[NDArray] = None
) -> rk45Output:
    
    y0 = np.asarray(y0)
    t_span = np.asarray(t_span)
    t0,tf = t_span
    status:int = 0
    message:str = ""
    ##find initial time_step if not given 
    if h0 is None:
        h0 = __auto_h0__(f,t_span,y0,rtol,atol,sys_params)
    
    max_steps = max(int((tf-t0)/h0), 10000000)

    try:
    ##integrate
        ts,ys,fs = integrate_core(
            t0,
            tf,
            y0,
            h0,
            max_steps,
            rtol,
            atol,
            f,
            sys_params
        )

        if t_eval is not None:
            t_uniform = t_eval
        else:
            if n is None:
                n = __auto_n__(ts,t_span,rtol)
                n = max(n,2*len(ts))

            t_uniform = np.linspace(t0,tf,n)
        
        ys_interpolated = interpolated_results(t_uniform,ts,ys,fs)
        event_times = []
        event_states = []
        if events is not None: # this part is not yet completed
            for _,event in enumerate(events):
                event_time,event_state = detect_event(ts,ys,event)
                event_times.append(event_time)
                event_states.append(event_state)
        status = 1
        message = "Integration successfully converged."

        return rk45Output(
            t = t_uniform, #type: ignore
            y = ys_interpolated, #type: ignore
            n_steps=len(ts), #type: ignore
            predicted_n= n,
            status = status,
            message=message
        )
    except RuntimeError as e:
        status = -1
        message = str(e)
        raise e




def detect_event(
        t:NDArray,
        y:NDArray,
        event:Callable
    ):
    g = np.array([event(ti,yi) for ti,yi in zip(t,y)])

    event_times,event_states = [],[]

    for i in range(len(g)-1):
        if g[i]*g[i-1] < 0:
            alpha = abs(g[i-1]) / (abs(g[i]) + abs(g[i-1]))

            t_event = t[i] + alpha*(t[i+1] - t[i])
            y_event = y[i] + alpha*(t[i+1]- t[i])

            event_times.append(t_event)
            event_states.append(event_states)
    return event_times,event_states


def refine_roots(t1,y1,t2,y2,max_iter=10):
    '''
    Bisection method to refine the time of events
    '''
    pass