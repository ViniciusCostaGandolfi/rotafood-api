package br.com.rotafood.api.modules.merchant.application.service;

import java.util.Comparator;
import java.util.List;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.function.Function;

public class SortIndexService {

    public static <T, ID> void adjustIndexesForUpdate(
            List<T> entities,
            ID entityId,
            int newIndex,
            Function<T, Integer> getIndex,
            BiConsumer<T, Integer> setIndex,
            Function<T, ID> getId,
            Consumer<List<T>> saveAll
    ) {
        entities.stream()
                .filter(e -> !getId.apply(e).equals(entityId))
                .sorted(Comparator.comparingInt(getIndex::apply))
                .forEachOrdered(e -> {
                    if (getIndex.apply(e) >= newIndex) {
                        setIndex.accept(e, getIndex.apply(e) + 1);
                    }
                });

        entities.stream()
                .filter(e -> getId.apply(e).equals(entityId))
                .findFirst()
                .ifPresent(e -> setIndex.accept(e, newIndex));

        saveAll.accept(entities);
    }
    
}
