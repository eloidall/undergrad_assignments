.data
prompt:         .asciiz "Please input an integer value greater than or equal to 0: "
intInput:       .asciiz "Your input: "
factResult:     .asciiz "The factorial is: "
repeatPrompt:   .asciiz "Would you like to do this again (Y/N): "
negInputError:  .asciiz "The value you entered is less than zero. This program only works with values greater than or equal to zero."
newLine:        .asciiz "\n"

.text
main:
    # Prompt user for input
    li $v0, 4
    la $a0, prompt
    syscall
    li $v0, 5
    syscall
    move $s1, $v0

    # Check if input is valid (>= 0)
    bltz $s1, exit_with_error

    # Factorial function call
    move $a0, $s1
    jal factorial
    move $t0, $v0

    # Print user input
    li $v0, 4
    la $a0, intInput
    syscall
    li $v0, 1
    move $a0, $s1
    syscall

    # Print factorial result
    li $v0, 4
    la $a0, newLine
    syscall
    li $v0, 4
    la $a0, factResult
    syscall
    li $v0, 1
    move $a0, $t0
    syscall

    # Ask user if they want to repeat
    li $v0, 4
    la $a0, newLine
    syscall
    li $v0, 4
    la $a0, repeatPrompt
    syscall

    # Read user choice
    li $v0, 12
    syscall
    # Check if user wants to repeat
    beq $v0, 89, repeat_main  # ASCII code for 'Y'

    # Exit program
    li $v0, 10
    syscall

# Repeat Main
repeat_main:
    li $v0, 14
    la $a0, 0
    li $a1, 100
    syscall
    j main

# Error Handling
exit_with_error:
    li $v0, 4
    la $a0, negInputError
    syscall
    li $v0, 10
    syscall

# Factorial Function
factorial:
    addi    $sp, $sp, -8
    sw      $s0, 4($sp)
    sw      $ra, 0($sp)
    bnez    $a0, else
    li      $v0, 1
    j       fact_return

else:
    move    $s0, $a0
    addi    $a0, $a0, -1
    jal     factorial
    multu   $s0, $v0
    mflo    $v0

fact_return:
    lw      $s0, 4($sp)
    lw      $ra, 0($sp)
    addi    $sp, $sp, 8
    jr      $ra
