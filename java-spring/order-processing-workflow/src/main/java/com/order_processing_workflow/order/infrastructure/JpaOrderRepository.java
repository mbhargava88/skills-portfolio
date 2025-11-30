package com.order_processing_workflow.order.infrastructure;

import com.order_processing_workflow.order.domain.Order;
import com.order_processing_workflow.order.domain.OrderRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JpaOrderRepository extends OrderRepository, JpaRepository<Order, Long> {
}
