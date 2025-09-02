package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.rotafood.api.modules.catalog.domain.entity.Category;

public interface CategoryRepository extends JpaRepository<Category, UUID>  {

    @Query("""
        SELECT DISTINCT c 
        FROM Category c
        LEFT JOIN FETCH c.items i
        LEFT JOIN FETCH i.product p
        WHERE c.merchant.id = :merchantId
        ORDER BY c.index
        """)
    List<Category> findAllByMerchantIdWithItems(@Param("merchantId") UUID merchantId);


    List<Category> findAllByMerchantId(UUID merchantId);
    
    Category findByIdAndMerchantId(UUID id, UUID merchantId);

    @Modifying
    @Query("UPDATE Category c SET c.index = :newIndex WHERE c.id = :categoryId AND c.merchant.id = :merchantId")
    void updateCategoryIndex(UUID merchantId, UUID categoryId, int newIndex);

}