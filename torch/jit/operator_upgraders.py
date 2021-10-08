"""
This is the centralized file for all PyTorch operator upgraders.
Each function definition here needs to following requirements:
1. The body of the function must be Torchscriptable
2. The naming convention of the upgraders should be:
    <op_name>_<op_overload>_upgrader_<old_version>_<new_version>
3. The name of the upgrader must be present in operator_versions.yaml
"""
import torch
import yaml

@torch.jit.script
def div_Tensor_0_3(self: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
    if (self.is_floating_point() or other.is_floating_point()):
        return self.true_divide(other)
    return self.divide(other, rounding_mode='trunc')

# def div_Scalar_0_3(self: Tensor, other: number) -> Tensor:
#     if (self.is_floating_point() or isinstance(other, float)):
#         return self.true_divide(other)
#     return self.divide(other, rounding_mode='trunc')

# # TODO: not present in the schema
# def div_0_3(self: number, other: number) -> number:
#     return self / other

# def div_out_0_3(self: Tensor, other: Tensor, *, out: Tensor) -> Tensor:
#     if (self.is_floating_point() or other.is_floating_point() or out.is_floating_point()):
#         return self.true_divide(other, out=out)
#     return self.divide(other, rounding_mode='trunc', out=out)

# def div__Tensor_0_3(self: Tensor, other: Tensor) -> Tensor:
#     if (self.is_floating_point() or other.is_floating_point()):
#         return self.true_divide_(other)
#     return self.divide_(other, rounding_mode='trunc')

# def div__Scalar_0_3(self: Tensor, other: number) -> Tensor:
#     if (self.is_floating_point() or isinstance(other, float)):
#         return self.true_divide_(other)
#     return self.divide_(other, rounding_mode='trunc')

# def full_names_0_4(size: List[int], fill_value: number, *, dtype: Optional[int] = None,
#              layout: Optional[int] = None, device: Optional[Device] = None,
#              pin_memory: Optional[bool] = None) -> Tensor:
#     if dtype is None:
#         fill_value = float(fill_value)
#     return torch.full(size, fill_value, dtype=dtype, layout=layout, device=device, pin_memory=pin_memory)

# def full_out_0_4(size: List[int], fill_value: number, *, out: Tensor) -> Tensor:
#     return torch.full(size, fill_value, out=out)

def listify(t):
    return list(map(listify, t)) if isinstance(t, (list, tuple)) else t

def format_bytecode(code_table):
    code_table_dict = {}
    for code in code_table:
        code_list = list(code)
        code_table_dict[code_list[0]] = listify(code_list[1:])
    return code_table_dict

if __name__ == "__main__":

    yaml_content = []
    div_tensor_0_3_mobile_code = torch._C.MobileCode(div_Tensor_0_3.graph, "div_Tensor_0_3")
    stream = open('bytecode.yaml', 'w')
    code_table = div_tensor_0_3_mobile_code.bytecode_table()
    formatted_code_table = format_bytecode(code_table)
    yaml_content.append({"div_Tensor_0_3": formatted_code_table})
    yaml.dump(yaml_content, stream)
