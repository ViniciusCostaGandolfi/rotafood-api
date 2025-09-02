package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.rotafood.api.modules.catalog.domain.entity.DefaultProduct;

public interface DefaultProductRepository extends JpaRepository<DefaultProduct, UUID> {
    @Query(value = "SELECT dp FROM DefaultProduct dp WHERE LOWER(dp.name) LIKE LOWER(CONCAT('%', :search, '%'))")
    List<DefaultProduct> findByNameContaining(@Param("search") String search, org.springframework.data.domain.Pageable pageable);
}
