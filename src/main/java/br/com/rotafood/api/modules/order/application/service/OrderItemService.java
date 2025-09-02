package br.com.rotafood.api.modules.order.application.service;

import br.com.rotafood.api.modules.catalog.domain.entity.Item;
import br.com.rotafood.api.modules.catalog.domain.entity.Option;
import br.com.rotafood.api.modules.merchant.domain.repository.ContextModifierRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.ItemRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.OptionRepository;
import br.com.rotafood.api.modules.order.application.dto.OrderItemDto;
import br.com.rotafood.api.modules.order.application.dto.OrderItemOptionDto;
import br.com.rotafood.api.modules.order.domain.entity.Order;
import br.com.rotafood.api.modules.order.domain.entity.OrderItem;
import br.com.rotafood.api.modules.order.domain.entity.OrderItemOption;
import br.com.rotafood.api.modules.order.domain.repository.OrderItemOptionRepository;
import br.com.rotafood.api.modules.order.domain.repository.OrderItemRepository;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Service
public class OrderItemService {

    @Autowired
    private ItemRepository itemRepository;

    @Autowired
    private OrderItemRepository orderItemRepository;

    @Autowired
    private OrderItemOptionRepository orderItemOptionRepository;

    @Autowired
    private OptionRepository optionRepository;

    @Autowired
    private ContextModifierRepository contextModifierRepository;

    @Transactional
    public OrderItem createOrUpdate(OrderItemDto orderItemDto, Order order) {

        Item catalogItem = itemRepository.findById(orderItemDto.item().id())
                .orElseThrow(() -> new EntityNotFoundException("Catalog item not found."));

        OrderItem orderItem = orderItemDto.id() != null
                ? orderItemRepository.findById(orderItemDto.id())
                        .orElseThrow(() -> new EntityNotFoundException("OrderItem not found."))
                : new OrderItem();

        orderItem.setItem(catalogItem);

        orderItem.setContextModifier(
                this.contextModifierRepository.findById(orderItemDto.contextModifierId())
                        .orElseThrow(() -> new EntityNotFoundException("Context modifier não encontrado!"))
                );

        orderItem.setQuantity(orderItemDto.quantity());

        orderItem.setTotalPrice(orderItemDto.totalPrice());

        orderItem.setObservations(orderItemDto.observations());

        order.getItems().add(orderItem);

        orderItemRepository.save(orderItem);

        if (orderItemDto.options() != null) {

            List<UUID> newOptionIds = orderItemDto.options().stream()
                    .map(OrderItemOptionDto::id)
                    .filter(Objects::nonNull)
                    .toList();

            orderItem.getOptions().removeIf(
                    existingOption -> existingOption.getId() != null && !newOptionIds.contains(existingOption.getId()));

            orderItemDto.options().forEach(optionDto -> this.createOrUpdateOption(optionDto, orderItem));
        }

        return orderItemRepository.save(orderItem);
    }

    @Transactional
    public OrderItemOption createOrUpdateOption(OrderItemOptionDto orderItemOptionDto, OrderItem orderItem) {

        OrderItemOption orderItemOption = orderItemOptionDto.id() != null
                ? orderItemOptionRepository.findById(orderItemOptionDto.id())
                        .orElse(new OrderItemOption())
                : new OrderItemOption();

        Option option = optionRepository.findById(orderItemOptionDto.option().id())
                .orElseThrow(() -> new EntityNotFoundException("Option not found."));

        orderItemOption.setQuantity(orderItemOptionDto.quantity());

        orderItemOption.setTotalPrice(orderItemOptionDto.totalPrice());

        orderItemOption.setContextModifier(
                this.contextModifierRepository.findById(orderItemOptionDto.contextModifierId())
                        .orElseThrow(() -> new EntityNotFoundException("Context modifier não encontrado!"))
                );

        orderItemOption.setOption(option);

        orderItem.getOptions().add(orderItemOption);

        return orderItemOptionRepository.save(orderItemOption);
    }

    @Transactional
        public void synchronizeItems(List<OrderItemDto> itemDtos, Order order) {
        List<UUID> newItemIds = itemDtos.stream()
                .map(OrderItemDto::id)
                .filter(Objects::nonNull)
                .toList();

        order.getItems().removeIf(existingItem ->
                existingItem.getId() != null && !newItemIds.contains(existingItem.getId()));

        itemDtos.forEach(itemDto -> this.createOrUpdate(itemDto, order));
        }

}
