package br.com.rotafood.api.modules.catalog.application.service;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.rotafood.api.modules.catalog.application.dto.ProductDto;
import br.com.rotafood.api.modules.catalog.domain.entity.Product;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.ProductRepository;

@Service
public class ProductService { 

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private MerchantRepository merchantRepository;

    @Autowired
    private ProductPackagingService productPackagingService;



    @Transactional
    public Product updateOrCreate(ProductDto productDto, UUID merchantId) {
        Merchant merchant = this.merchantRepository.getReferenceById(merchantId);
    
        Product product = productDto.id() != null
                ? productRepository.findById(productDto.id()).orElse(new Product())
                : new Product();
    
        product.setMerchant(merchant);
        product.setName(productDto.name());
        product.setDescription(productDto.description());
        product.setEan(productDto.ean());
        product.setAdditionalInformation(productDto.additionalInformation());
        product.setImagePath(productDto.imagePath());
        product.setServing(productDto.serving());
        product.setPackagingType(productDto.packagingType());
        product.setQuantity(productDto.quantity());

        productRepository.save(product);
    
    
        if (productDto.packaging() != null) {
            product.setProductPackaging(productPackagingService.createOrUpdate(productDto.packaging(), merchantId));
        }
    
        return product;
    }
    


    @Transactional
    public void deleteById(UUID productId, UUID merchantId) {
            Product product = productRepository.findByIdAndMerchantId(productId, merchantId);
            productRepository.delete(product);
    }

    public Product getById(UUID productId, UUID merchantId) {
        return productRepository.findByIdAndMerchantId(productId, merchantId);
    }

    public List<Product> getAll(UUID merchantId) {
        return productRepository.findAllByMerchantId(merchantId);
    }
}
