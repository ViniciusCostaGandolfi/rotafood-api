package br.com.rotafood.api.modules.order.domain.entity;

public enum OrderStatus {
    CREATED,              
    CONFIRMED,            
    PREPARATION_STARTED,  
    READY_TO_PICKUP,       
    DISPATCHED,           
    COMPLETED,            
    CANCELED              
}