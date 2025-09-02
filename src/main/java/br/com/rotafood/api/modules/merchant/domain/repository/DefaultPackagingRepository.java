package br.com.rotafood.api.modules.merchant.domain.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.domain.Page;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.rotafood.api.modules.catalog.domain.entity.DefaultPackaging;

public interface DefaultPackagingRepository extends JpaRepository<DefaultPackaging, UUID> {
    @Query(value = "SELECT dp FROM DefaultPackaging dp WHERE LOWER(dp.name) LIKE LOWER(CONCAT('%', :search, '%'))")
    List<DefaultPackaging> findByNameContaining(@Param("search") String search, org.springframework.data.domain.Pageable pageable);

    Page<DefaultPackaging> findAll(org.springframework.data.domain.Pageable pageable);

}
