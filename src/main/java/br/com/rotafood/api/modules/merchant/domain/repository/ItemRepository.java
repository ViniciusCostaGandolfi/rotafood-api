package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import br.com.rotafood.api.modules.catalog.domain.entity.Item;

public interface ItemRepository extends JpaRepository<Item, UUID> {

    Optional<Item> findByIdAndMerchantId(UUID id, UUID merchantId);

    List<Item> findAllByMerchantId(UUID merchantId);

    void deleteByCategoryId(UUID categoryId);

    @Modifying
    @Query("UPDATE Item i SET i.index = :newIndex WHERE i.id = :itemId AND i.category.id = :categoryId")
    void updateItemIndex(UUID categoryId, UUID itemId, int newIndex);


}
 