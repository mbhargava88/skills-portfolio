package com.order_processing_workflow.order.domain;


public enum OrderStatus {
    PENDING,
    VALIDATED,
    STOCK_CONFIRMED,
    PAYMENT_CAPTURED,
    SENT_FOR_DELIVERY,
    COMPLETED,
    FAILED
}