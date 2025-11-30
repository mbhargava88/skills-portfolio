package com.order_processing_workflow.order.domain;

import com.order_processing_workflow.order.domain.Order;
import java.util.Optional;

public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(Long id);
}


