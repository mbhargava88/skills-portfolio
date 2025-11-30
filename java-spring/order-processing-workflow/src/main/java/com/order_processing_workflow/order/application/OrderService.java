package com.order_processing_workflow.order.application;

import com.order_processing_workflow.order.domain.Order;

import java.util.Optional;

public interface OrderService {
    Order placeOrder(String customerName);
    Optional<Order> getOrder(Long id);
}
