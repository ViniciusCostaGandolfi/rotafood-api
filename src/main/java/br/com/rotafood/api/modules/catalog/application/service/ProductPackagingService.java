package br.com.rotafood.api.modules.catalog.application.service;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.rotafood.api.modules.catalog.application.dto.ProductPackagingDto;
import br.com.rotafood.api.modules.catalog.domain.entity.Packaging;
import br.com.rotafood.api.modules.catalog.domain.entity.ProductPackaging;
import br.com.rotafood.api.modules.merchant.domain.repository.ProductPackagingRepository;
import jakarta.persistence.EntityNotFoundException;

@Service
public class ProductPackagingService {


    @Autowired 
    private PackagingService packagingService;
    @Autowired 
    private ProductPackagingRepository productPackagingRepository;


    @Transactional
    public ProductPackaging createOrUpdate(ProductPackagingDto productPackagingDto, UUID merchantId) {
        Packaging packaging = packagingService.updateOrCreate(productPackagingDto.packaging(), merchantId);

        ProductPackaging productPackaging = productPackagingDto.id() != null
            ? productPackagingRepository.findById(productPackagingDto.id())
                .orElse(new ProductPackaging())
            : new ProductPackaging();

        productPackaging.setPackaging(packaging);
        productPackaging.setQuantityPerPackage(productPackagingDto.quantityPerPackage());

        return productPackagingRepository.save(productPackaging);
    }


    @Transactional
    public void delete(UUID productPackagingId) {
        ProductPackaging productPackaging = productPackagingRepository.findById(productPackagingId)
                .orElseThrow(() -> new EntityNotFoundException("Relação Produto-Embalagem não encontrada."));
        productPackagingRepository.delete(productPackaging);
    }

    @Transactional
    public void deleteAll(List<ProductPackaging> productPackagings) {
        productPackagingRepository.deleteAll(productPackagings);
    }
}
