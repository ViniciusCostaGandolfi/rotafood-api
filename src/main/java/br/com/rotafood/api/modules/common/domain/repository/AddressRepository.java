package br.com.rotafood.api.modules.common.domain.repository;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.rotafood.api.modules.common.domain.entity.Address;

public interface AddressRepository extends JpaRepository<Address, UUID> {
    Optional<Address> findFirstByPostalCode(String postalCode);

    Optional<Address> findFirstByFormattedAddressContainingIgnoreCase(String q);

    List<Address> findByFormattedAddressContainingIgnoreCase(String q);


}

