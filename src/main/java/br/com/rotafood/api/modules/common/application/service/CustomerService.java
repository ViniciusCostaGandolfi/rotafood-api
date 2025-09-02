package br.com.rotafood.api.modules.common.application.service;

import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.common.application.dto.CustomerDto;
import br.com.rotafood.api.modules.common.domain.entity.Address;
import br.com.rotafood.api.modules.common.domain.entity.Customer;
import br.com.rotafood.api.modules.common.domain.entity.CustomerAddress;
import br.com.rotafood.api.modules.common.domain.repository.AddressRepository;
import br.com.rotafood.api.modules.common.domain.repository.CustomerRepository;

import java.util.Optional;

@Service
public class CustomerService {

    @Autowired
    private CustomerRepository customerRepository;

    @Autowired
    private AddressRepository addressRepository;

    public Optional<Customer> getByPhone(String phone) {
        return customerRepository.findByPhone(phone);
    }

    @Transactional
    public Customer createOrUpdateWithAddressIfDelivery(CustomerDto dto, AddressDto addressDto) {
        
        Customer customer = customerRepository.findByPhone(dto.phone())
                .orElseGet(() -> {
                    Customer newCustomer = new Customer();
                    newCustomer.setPhone(dto.phone());
                    return newCustomer;
                });
        
        

        customer.setName(dto.name());

        if (addressDto != null) {
            Address address = addressDto.id() != null
                    ? this.addressRepository.findById(addressDto.id()).orElseThrow(() -> new EntityNotFoundException("Endereço não encontrado"))
                    : this.addressRepository.save(new Address(addressDto));

            boolean alreadyLinked = customer.getAddresses().stream()
                    .anyMatch(ca -> ca.getAddress().getId().equals(address.getId()));

            if (!alreadyLinked) {
                CustomerAddress ca = new CustomerAddress();
                ca.setCustomer(customer);
                ca.setAddress(address);
                customer.getAddresses().add(ca);
            }
        }

        return customerRepository.save(customer);
    }


}
