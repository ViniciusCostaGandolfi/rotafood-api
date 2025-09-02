package br.com.rotafood.api.modules.common.application.controller.v1;

import jakarta.persistence.EntityNotFoundException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.rotafood.api.modules.common.application.dto.FullCustomerDto;
import br.com.rotafood.api.modules.common.application.service.CustomerService;

@RestController
@RequestMapping(ApiVersion.VERSION + "/customers")
public class CustomerController {

    @Autowired
    private CustomerService customerService;

    @GetMapping("/phone/{phone}")
    public FullCustomerDto getCustomerByPhone(@PathVariable String phone) {
        return customerService.getByPhone(phone)
                .map(FullCustomerDto::new)
                .orElseThrow(() -> new EntityNotFoundException("Customer not found"));
    }
}
