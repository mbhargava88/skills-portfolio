package com.order_processing_workflow.order.application;

import com.order_processing_workflow.order.domain.Order;
import com.order_processing_workflow.order.domain.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class OrderServiceImpl implements OrderService {

    @Autowired
    private final OrderRepository repository;

    public OrderServiceImpl(OrderRepository repository) {
        this.repository = repository;
    }

    @Override
    public Order placeOrder(String customerName) {
        Order order = new Order(customerName);
        return repository.save(order);
    }

    @Override
    public Optional<Order> getOrder(Long id) {
        return repository.findById(id);
    }
}